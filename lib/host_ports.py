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

   def generate_tor_links(self, tor_name, rack):
      tor_links = [] 
      required_ports = rack.ports.count
      for rport in rack.ports.ports_list:
         for sport in self.ports_list:
            if sport['in_use'] is False and self.is_form_factor_compatible(sport['form_factor'],rport['form_factor']):
               if self.is_intersect(rport['speeds'],sport['speeds']):
                  speed = rport['speeds'][0]
                  sport['in_use'] = True
                  tor_links.append(Link(tor_name, sport['name'], sport['form_factor'], speed))
                  tor_links[len(tor_links)-1].set_remote_vars("host","host_port",sport['form_factor'],speed)
                  required_ports -= 1
                  break
      ###Reset in_use flag
      for sport in self.ports_list:
         sport['in_use'] = False
      if required_ports > 0:
         util.log_error_and_exit("generate_tor_links() failed to generate links for TOR "+tor_name)
      else:
         return tor_links
