import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
import util
from ports import Ports
from link import Link
class Host_ports(Ports):
   def __init__(self, ports_list):
      self.ports_list = []
      self.count = 0
      for port in ports_list:
         for key in self.required_rack_keys:
            if not port.has_key(key):
	       util.log_error_and_exit("Rack SKU host_network_interfaces definition is missing key "+key)
      for port in ports_list:
         for count in range(0, int(port['count'])):
            port_definition = { 'name': self.count, 'form_factor': port['form_factor'], 'speeds': [ port['speed'] ], 'breakouts': [], 'port_group': self.count, 'in_use': False }
            self.ports_list.append(port_definition)
            self.count += 1
