import argparse
import sys
import os
import csv
import yaml
import util
import math

class Network_interfaces:
   required_keys = [
      "speed",
      "optic",
      "mtu",
      "count" ]
   supported_speeds = [
      1,
      10,
      25,
      100,
      400 ]
   supported_optics = [
      "RJ45",
      "SFP",
      "SFPP",
      "SFPP-T",
      "SFP28",
      "QSFP",
      "QSFPP",
      "QSFP28",
      "QSFP56-DD" ]
   def __init__(self, network_interfaces_dict, rack_name):
      for key in required_keys:
         if not network_interfaces_dict.has_key(key):
            util.log_error_and_exit("Missing key of "+str(key)+" from configuration for rack "+str(rack_name)
      if network_interfaces_dict['speed'] not in supported_speeds:
            util.log_error_and_exit("Network interface speed of "+str(network_interfaces_dict['speed'])+" is not supported")
      if network_interfaces_dict['optic'] not in supported_optics:
            util.log_error_and_exit("Network interface optic of "+str(network_interfaces_dict['optic'])+" is not supported")
      for key, value in network_interfaces_dict.items():
         setattr(self, key, value)

