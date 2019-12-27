import yaml
import sys
import logging
import click_log

from illuminatio.test_case import NetworkTestCase
from illuminatio.host import ClusterHost, GenericClusterHost


def parse_manual_tests(test_input, logger):

   testcases = []

   try:
       allinputs = yaml.safe_load_all(open(test_input))
   except Exception as error:
       logger.error(error)
       sys.exit()

   logger.info("Using %s as test input..." % test_input)

   # Create a map of src_type value (pod, namespace, etc.) to the actual object (ClusterHost, GenericClusterHost, etc.)
   # case is a NetworkTestCase object with 4 parameters (src obj, dst obj, ports, action)
   # testcases is a list of all cases
   map_dict = {'pod': ClusterHost, 'namespace': GenericClusterHost}
   map_act  = {'allow': True, 'deny': False}
   for value in allinputs:
       if value:
           validate_testinput_schema(value)
           logger.info(value)

           case = NetworkTestCase(
                   map_dict[value['src_type']](value['src_namespace'], value['src_selector']),
                   map_dict[value['dest_type']](value['dest_namespace'], value['dest_selector']),
                   value['ports'],
                   map_act[value['action']]
                   )

           logger.info(case)
           testcases.append(case)


   return testcases

# todo
def validate_testinput_schema(case):
   pass

if __name__ == "__main__":

   LOGGER = logging.getLogger(__name__)
   click_log.basic_config(LOGGER)

   parse_manual_tests("tests.yaml", LOGGER)
