import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
import util
from link import Link
class Ports:
   ###Used to represent the various capabilities of a platform's dataplane interfaces
   required_sku_keys = [
      "name",
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
   def __init__(self, ports_list):
      self.ports_list = []
      self.count = 0
      for port in ports_list:
         for key in self.required_sku_keys:
            if not port.has_key(key):
               util.log_error_and_exit("Platform SKU network interfaces definition is missing key "+key)
      for port in ports_list:
         port['in_use'] = False
         self.ports_list.append(port)
         self.count += 1

   def can_support_rack_port_requirements(self, rack):
      ###FIXME Add support for breakouts
      required_ports = rack.host_ports.count + rack.fabric_ports.count
      rport_list = rack.host_ports.ports_list + rack.fabric_ports.ports_list
      for rport in rport_list:
         for sport in self.ports_list:
            if sport['in_use'] is False and self.is_form_factor_compatible(sport['form_factor'],rport['form_factor']): 
               if self.is_intersect(rport['speeds'],sport['speeds']):
                  sport['in_use'] = True
                  required_ports -= 1
                  break
      ###Reset in_use flag
      for sport in self.ports_list:
         sport['in_use'] = False
      if required_ports > 0:
         return False
      else:
         return True

   def can_support_link_requirements(self, links):
      required_ports = len(links)
      for link in links:
         for sport in self.ports_list:
            if sport['in_use'] is False and self.is_form_factor_compatible(sport['form_factor'],link.local_form_factor):
               if link.local_speed in sport['speeds']:
                  sport['in_use'] = True
                  required_ports -= 1
                  break
      ###Reset in_use flag
      for sport in self.ports_list:
         sport['in_use'] = False
      if required_ports > 0:
         return False
      else:
         return True

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
