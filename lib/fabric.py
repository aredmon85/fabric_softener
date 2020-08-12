import argparse
import sys
import os
import csv
import yaml
import util
import math
import copy
from stage import Stage
from tor import Tor
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
   current_stage = 0
   stages = []
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
      northbound_ports = []
      for rack in self.racks:
         for idx in range(0,rack.rack_count):
            sku = platform_engine.get_matching_tors_for_reqs(rack)
            tors.append(Tor(rack,idx,sku))        
            #southbound_ports.append(rack.fabric_ports)
      #self.stages.append(Stage(self.current_stage, southbound_ports, 1))
      #self.stages[self.current_stage].devices = copy.deepcopy(tors)
      #self.current_stage += 1
      print "A total of "+str(len(tors))+" TORs has been created"
  
   def generate_fabric(self, platform_engine):
      tors = []
      southbound_ports = []
      self.build_tors(platform_engine)
      ###Generate T1
      for rack in self.racks:
         for idx in range(0,rack.rack_count):
            southbound_ports.append(rack.fabric_ports)
            tors.append(Tor(rack,idx,sku))
      self.stages.append(Stage(self.current_stage, southbound_ports, 1))
      self.stages[self.current_stage].devices = copy.deepcopy(tors)
      self.current_stage += 1



   
      
