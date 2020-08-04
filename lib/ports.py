import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
import util
class Ports:
   required_sku_keys = [
      "form_factor",
      "speeds",
      "breakouts", 
      "port_group"
   ]
   required_rack_keys = [
      "speed",
      "form_factor",
      "count"
   ]
   speeds = [
      1,
      10,
      25,
      40,
      50,
      100,
      400 ]
   form_factors = [
      "RJ45",
      "SFP",
      "SFPP",
      "SFPP-T",
      "SFP28",
      "QSFP",
      "QSFPP",
      "QSFP28",
      "QSFP56-DD" ]
   ports_list = None
   count = None
   def __init__(self, ports_list, is_rack):
      self.ports_list = []
      self.count = 0
      if is_rack is False:
         for port in ports_list:
            for key in self.required_sku_keys:
               if not port.has_key(key):
                  util.log_error_and_exit("Platform SKU network interfaces definition is missing key "+key)
         for port in ports_list:
            port['in_use'] = False
            self.ports_list.append(port)
            self.count += 1

      else:
         for port in ports_list:
            for key in self.required_rack_keys:
               if not port.has_key(key):
                  util.log_error_and_exit("Rack SKU host_network_interfaces definition is missing key "+key)
         for port in ports_list:
            for count in range(0, int(port['count'])):
               port_definition = { 'form_factor': port['form_factor'], 'speeds': [ port['speed'] ], 'breakouts': [], 'port_group': self.count, 'in_use': False }
               self.ports_list.append(port_definition)
               self.count += 1

   def can_support_port_requirements(self, rack):
      required_ports = rack.ports.count
      for rport in rack.ports.ports_list:
         for sport in self.ports_list:
            if sport['in_use'] is False and self.is_form_factor_compatible(sport['form_factor'],rport['form_factor']): 
               if self.is_intersect(rport['speeds'],sport['speeds']):
                  sport['in_use'] = True
                  required_ports -= 1
                  break

      if required_ports > 0:
         return False
      else:
         return True

   def update_uplink_ports(self,total_required_fabric_network_capacity,largest_potential_flow_size):
      ###Determine the uplink speed based on the largest potential flow size
      ###FIXME We should also factor in cost, and support exploring multiple uplink speed options here
      ###Determine number of uplinks based on total_required_fabric_network_capacity of the rack, with a floor of 2 (2 is the minimum number of uplinks we'll support)
      print "Creating uplink ports"
      links = []
      port_group = len(self.ports_list)
      if largest_potential_flow_size >= 100:
         target_uplink_speed = 400
         link_count = int(max((total_required_fabric_network_capacity / 400),2))
         for link in range(0,link_count):
            links.append({'form_factor': 'QSFP56-DD', 'speeds': [400], 'breakouts': [], 'port_group': port_group, 'in_use': False })
            port_group += 1
      else:
         target_uplink_speed = 100
         link_count = int(max(total_required_fabric_network_capacity / 100,2))
         for link in range(0,link_count):
            links.append({'form_factor': 'QSFP28', 'speeds': [100], 'breakouts': [], 'port_group': port_group, 'in_use': False })
            port_group += 1
      for link in links:
         self.ports_list.append(link)

   def is_form_factor_compatible(self,left_form_factor,right_form_factor):
      if left_form_factor == right_form_factor:
         return True
      if left_form_factor == 'SFPP' and right_form_factor == 'SFP28':
         return True
      if right_form_factor == 'SFPP' and left_form_factor == 'SFP28':
         return True
      if right_form_factor == 'SFPP-T' and left_form_factor == 'SFP28':
         return True
      return False

   def is_intersect(self,list1,list2):
      for i in list1:
         if i in list2:
            return True
      return False
