"""
This is a simple example of how to use the PyE2 library.

In this example, we connect to the network, choose a node and
    deploy a plugin with custom code that will run in real time.
    
For this example, we search for prime numbers in parallel using more than one node.
"""
from PyE2 import Session, CustomPluginTemplate
from PyE2 import DistributedCustomCodePresets as Presets


def custom_code_remote_node(plugin: CustomPluginTemplate):
  """
  The custom code that will be executed on the main thread.

  Parameters
  ----------
  plugin : CustomPluginTemplate
      The plugin instance. It will be replaced with the plugin instance object on the remote side.

  Returns
  -------
  list
      The result of the custom code.
      In our case, the list of prime numbers found in the random numbers generated.
  """

  def is_prime(n):
    if n <= 1:
      return False
    for i in range(2, int(plugin.np.sqrt(n)) + 1):
      if n % i == 0:
        return False
    return True

  random_numbers = plugin.np.random.randint(0, 5000, 20)

  are_primes = plugin.threadapi_map(is_prime, random_numbers, n_threads=2)

  prime_numbers = []
  for i in range(len(random_numbers)):
    if are_primes[i]:
      prime_numbers.append(random_numbers[i])

  return prime_numbers


def on_data(pipeline, full_payload):
  progress = full_payload.get('PROGRESS')
  data = full_payload.get('DATA')
  len_data = 0
  if data:
    data.sort()
    len_data = len(data)

  pipeline.P(f"Progress: {progress} -- Found: {len_data} -- Primes: {data}\n\n")


if __name__ == "__main__":
  s = Session()

  node = "stefan-box-ee"
  s.wait_for_node(node)

  # This should be in #132
  p = s.create_or_attach_to_pipeline(
    node_id=node,
    name="run_distributed",
    data_source="Void"
  )

  p.create_distributed_custom_plugin_instance(
    instance_id="run_distributed_2",
    custom_code_process_real_time_collected_data=Presets.process_real_time_collected_data__keep_uniques_in_aggregated_collected_data,
    custom_code_finish_condition=Presets.finish_condition___aggregated_data_more_than_X,
    finish_condition_kwargs={
      "X": 100
    },
    custom_code_aggregate_collected_data=Presets.aggregate_collected_data___aggregate_collected_data,

    custom_code_remote_node=custom_code_remote_node,
    node_pipeline_config={
      'stream_type': "Void",
    },
    node_plugin_config={
      "PROCESS_DELAY": 1,
    },
    nr_remote_nodes=2,
    on_data=on_data
  )

  p.deploy()

  s.run(wait=True, close_pipelines=True)

  # TODO: print text when job is launched
  # TODO: print workers found
