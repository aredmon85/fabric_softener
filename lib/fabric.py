import argparse
import sys
import os
import csv
import yaml
import util
import math
import copy
import util as util
from link import Link
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
   network_addressing = None  
   rack_id = 0
   current_stage = 0
   stages = []
   render_config = {}
   links = []
   devices = [] 
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
      self.network_addressing = Network_addressing(fabric_config_dict['fabric']['addressing']) 
      print "Total rack facing capacity required: "+str(self.rack_facing_capacity)
      print "Total edge facing capacity required: "+str(self.edge_facing_capacity)
   
   def generate_tor_links(self, tor, rack):
      tor_links = []
      required_ports = rack.host_ports.count
      rport_list = rack.host_ports.ports_list
      for rport in rport_list:
         for sport in tor.sku.ports.ports_list:
            if sport['in_use'] is False and util.is_form_factor_compatible(sport['form_factor'],rport['form_factor']):
               if util.is_intersect(rport['speeds'],sport['speeds']):
                  speed = rport['speeds'][0]
                  sport['in_use'] = True
                  tor_links.append(Link(tor.name, sport['name'], sport['form_factor'], speed))
                  tor_links[len(tor_links)-1].set_remote_vars("host","host_port",sport['form_factor'],speed)
                  required_ports -= 1
                  break

      required_ports = rack.fabric_ports.count
      rport_list = rack.fabric_ports.ports_list
      for rport in rport_list:
         for sport in tor.sku.ports.ports_list:
            if sport['in_use'] is False and util.is_form_factor_compatible(sport['form_factor'],rport['form_factor']):
               if util.is_intersect(rport['speeds'],sport['speeds']):
                  speed = rport['speeds'][0]
                  sport['in_use'] = True
                  tor_links.append(Link(tor.name, sport['name'], sport['form_factor'], speed))
                  tor_links[len(tor_links)-1].set_remote_vars("next_stage","next_stage",sport['form_factor'],speed)
                  required_ports -= 1
                  break

      ###Reset in_use flag
      for sport in tor.sku.ports.ports_list:
         sport['in_use'] = False
      if required_ports > 0:
         util.log_error_and_exit("generate_tor_links() failed to generate links for TOR "+tor_name)
      else:
         return tor_links

   def build_tor_stage(self, platform_engine, sub_ratio):
      tors = []
      north_links = [] 
      for rack in self.racks:
         for idx in range(0,rack.rack_count):
            sku = platform_engine.get_matching_tors_for_reqs(rack)
            tor = Tor(rack,idx,sku)
            tors.append(tor)
            self.devices.append(tor)
            tor_links = self.generate_tor_links(tor,rack)
            for link in tor_links:
               north_links.append(link)
      tor_stage = Stage(0,tors,platform_engine,self.edge_facing_capacity,sub_ratio)
      tor_stage.devices = copy.deepcopy(tors)
      tor_stage.north_links_list = copy.deepcopy(north_links)
      print "A total of "+str(len(tors))+" TORs has been created"
      return tor_stage
            
   def generate_fabric(self,platform_engine):
      fabric_config = [] 
      self.stages.append(self.build_tor_stage(platform_engine,1))
      ###Generate T1
      while self.stages[self.current_stage].additional_stage_required == True:
      	 self.current_stage += 1
         self.stages.append(Stage(self.current_stage,self.stages[self.current_stage-1].north_links_list,platform_engine,self.edge_facing_capacity,1))
         self.devices += self.stages[self.current_stage].devices
      for stage in self.stages:
         if len(stage.links) > 0:
            self.links += stage.links
      network_addr_idx = 0
      for link in self.links:
         ###FIXME: Lord forgive these sins
         link.local_address = str(self.network_addressing.network_point_to_point_subnets[network_addr_idx][0])+"/31"
         link.remote_address = str(self.network_addressing.network_point_to_point_subnets[network_addr_idx][1])+"/31"
         link.subnet = str(self.network_addressing.network_point_to_point_subnets[network_addr_idx])
         #print link.local_device + ":" + link.local_port + ":" + link.local_address + ":" + link.remote_device + ":" + link.remote_port + ":" + link.remote_address + ":" + link.subnet
         network_addr_idx += 1
      network_addr_idx = 0
      for dev in self.devices:
         dev.loopback_address = str(self.network_addressing.loopbacks_subnets[network_addr_idx])
         dev.management_network_address = str(self.network_addressing.management_network_subnets[network_addr_idx])
         config = {}
         config['device'] = dev
         config['links'] = []
         for link in self.links:
            if link.local_device == dev.name:
               config['links'].append(link)
         network_addr_idx += 1
         fabric_config.append(config)
      return fabric_config
    
