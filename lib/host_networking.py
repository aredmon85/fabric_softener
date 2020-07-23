import argparse
import sys
import os
import csv
import yaml
import util
import math

class Host_networking:
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
   
   host_interfaces_total = {}
   def __init__(self, network_interfaces_list, rack_name):
      for key in self.supported_optics:
         self.host_interfaces_total[key] = 0

      for nic in network_interfaces_list:
         for key in self.required_keys:
            if not nic.has_key(key):
               util.log_error_and_exit("Missing key of "+str(key)+" from configuration for rack "+str(rack_name))
         if nic['speed'] not in self.supported_speeds:
            util.log_error_and_exit("Network interface speed of "+str(nic['speed'])+" is not supported")
         if nic['optic'] not in self.supported_optics:
            util.log_error_and_exit("Network interface optic of "+str(nic['optic'])+" is not supported")
         self.host_interfaces_total[nic['optic']] += 1 * nic['count']
