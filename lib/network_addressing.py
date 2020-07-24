import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
class Network_addressing:
   required_keys = [
      "network_point_to_points",
      "loopbacks",
      "management_network" ]
   network_point_to_point_network = None
   network_point_to_point_subnets = None
   network_point_to_point_exclude = []
   loopbacks_network = None
   loopbacks_addresses = None
   loopbacks_exclude = []
   management_network_network = None
   management_network_addresses = None
   management_network_exclude = []

   def __init__(self, addressing_config_dict):
      for key in self.required_keys:
         if not addressing_config_dict.has_key(key):
            util.log_error_and_exit("Addressing configuration is missing "+key)
     
      ###Populate lists of available subnets and addresses
      ###FIXME: Add IPv6 support
      self.network_point_to_point_network = ipaddress.IPv4Network(unicode(addressing_config_dict['network_point_to_points']['range']),strict=True)
      self.network_point_to_point_subnets = list(self.network_point_to_point_network.subnets(new_prefix=31))
      if addressing_config_dict['network_point_to_points'].has_key('exclude'):
         for addr in addressing_config_dict['network_point_to_points']['exclude']: 
            if not util.is_ip_address(addr):
               if not util.is_ip_network(addr):
                  util.log_error_and_exit("Excluded address "+addr+" is not a valid IP address or network")
            self.network_point_to_point_exclude.append(ipaddress.IPv4Network(unicode(addr)))
      
         ###Remove any subnets that contain excluded addresses
         ###FIXME: I'm lazy and not doing LPM
         for addr in self.network_point_to_point_exclude:
            for subnet in self.network_point_to_point_subnets:
               if subnet.overlaps(addr):
                  print "Excluding subnet: "+str(subnet)
                  self.network_point_to_point_subnets.remove(subnet)

      ###Populate lists of available subnets and addresses
      ###FIXME: Add IPv6 support
      self.loopbacks_network = ipaddress.IPv4Network(unicode(addressing_config_dict['loopbacks']['range']),strict=True)
      self.loopbacks_subnets = list(self.loopbacks_network.subnets(new_prefix=32))
      if addressing_config_dict['loopbacks'].has_key('exclude'):
         for addr in addressing_config_dict['loopbacks']['exclude']:
            if not util.is_ip_address(addr):
               if not util.is_ip_network(addr):
                  util.log_error_and_exit("Excluded address "+addr+" is not a valid IP address or network")
            self.loopbacks_exclude.append(ipaddress.IPv4Network(unicode(addr)))

         ###Remove any subnets that contain excluded addresses
         ###FIXME: I'm lazy and not doing LPM
         for addr in self.loopbacks_exclude:
            for subnet in self.loopbacks_subnets:
               if subnet.overlaps(addr):
                  print "Excluding subnet: "+str(subnet)
                  self.loopbacks_subnets.remove(subnet)

      ###Populate lists of available subnets and addresses
      ###FIXME: Add IPv6 support
      self.management_network_network = ipaddress.IPv4Network(unicode(addressing_config_dict['management_network']['range']),strict=True)
      self.management_network_subnets = list(self.management_network_network.subnets(new_prefix=32))
      if addressing_config_dict['management_network'].has_key('exclude'):
         for addr in addressing_config_dict['management_network']['exclude']:
            if not util.is_ip_address(addr):
               if not util.is_ip_network(addr):
                  util.log_error_and_exit("Excluded address "+addr+" is not a valid IP address or network")
            self.management_network_exclude.append(ipaddress.IPv4Network(unicode(addr)))

         ###Remove any subnets that contain excluded addresses
         ###FIXME: I'm lazy and not doing LPM
         for addr in self.management_network_exclude:
            for subnet in self.management_network_subnets:
               if subnet.overlaps(addr):
                  print "Excluding subnet: "+str(subnet)
                  self.management_network_subnets.remove(subnet)
 
