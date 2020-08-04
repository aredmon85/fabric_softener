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
      "form_factor",
      "mtu",
      "count" ]
   supported_speeds = [
      1,
      10,
      25,
      40,
      50,
      100,
      400 ]
   supported_form_factors = [
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
      for key in self.supported_form_factors:
         self.host_interfaces_total[key] = 0

      for nic in network_interfaces_list:
         for key in self.required_keys:
            if not nic.has_key(key):
               util.log_error_and_exit("Missing key of "+str(key)+" from configuration for rack "+str(rack_name))
         if nic['speed'] not in self.supported_speeds:
            util.log_error_and_exit("Network interface speed of "+str(nic['speed'])+" is not supported")
         if nic['form_factor'] not in self.supported_form_factors:
            util.log_error_and_exit("Network interface form_factor of "+str(nic['optic'])+" is not supported")
         self.host_interfaces_total[nic['form_factor']] += 1 * nic['count']

