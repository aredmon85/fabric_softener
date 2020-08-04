import argparse
import sys
import os
import csv
import yaml
import util
import math
from rack import Rack
from network_addressing import Network_addressing
class Fabric:
   required_keys = [
      "edge_facing_capacity",
      "racks",
      "addressing" ]
   racks = []
   total_racks = 0
   edge_facing_capacity = 0
   rack_facing_capacity = 0
   addressing = []  
   rack_id = 0
   def __init__(self, fabric_config_dict):
      
      if fabric_config_dict.has_key("fabric"):
         for key in self.required_keys:
            if not fabric_config_dict['fabric'].has_key(key):
               util.log_error_and_exit("Fabric configuration file is missing "+key)
         
         try:
            self.edge_facing_capacity = int(fabric_config_dict["fabric"]["edge_facing_capacity"])
         except ValueError:
            util.log_error_and_exit("Invalid value found for total edge facing capacity in provided fabric configuration")

         for rack in fabric_config_dict['fabric']['racks']:
            rack['rack_id'] = self.rack_id
            self.total_racks += rack['rack_count']
            self.racks.append(Rack(rack))
            self.rack_facing_capacity += self.racks[self.rack_id].total_required_fabric_network_capacity * self.racks[self.rack_id].rack_count
            self.rack_id += 1

      network_addressing = Network_addressing(fabric_config_dict['fabric']['addressing']) 
      print "Total rack facing capacity required: "+str(self.rack_facing_capacity)
      print "Total edge facing capacity required: "+str(self.edge_facing_capacity)
 
   def build_tors(self, platform_engine):
     tors = [] 
     for rack in self.racks:
         tors.append(platform_engine.get_matching_tors_for_reqs(rack))
