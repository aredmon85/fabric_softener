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
class Fabric_ports(Ports):
   def __init__(self, total_required_fabric_network_capacity, largest_potential_flow_size):
      self.ports_list = []
      self.count = 0
      links = []
      port_group = len(self.ports_list)
      if largest_potential_flow_size >= 100:
         target_spine_speed = 400
         link_count = int(max((total_required_fabric_network_capacity / 400),2))
         for link in range(0,link_count):
            links.append({'form_factor': 'QSFP56-DD', 'speeds': [400], 'breakouts': [], 'port_group': port_group, 'in_use': False })
            port_group += 1
      else:
         target_spine_speed = 100
         link_count = int(max(total_required_fabric_network_capacity / 100,2))
         for link in range(0,link_count):
            links.append({'form_factor': 'QSFP28', 'speeds': [100], 'breakouts': [], 'port_group': port_group, 'in_use': False })
            port_group += 1
      for link in links:
         self.ports_list.append(link)

