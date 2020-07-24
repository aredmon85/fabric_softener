import argparse
import sys
import os
import csv
import yaml
import util
import math
from host_networking import Host_networking
class Rack:
   required_attributes = [
      "rack_id", 
      "name",
      "rack_count", 
      "power_current", 
      "airflow_direction", 
      "vxlan_required",
      "host_network_interfaces",
      "subscription_ratio_to_fabric", 
      "power_available_for_network" ]

   tors = [] 
   total_required_host_network_capacity = 0
   total_required_fabric_network_capacity = 0  
   rack_host_networking = None
   rack_count = 0
   ###It's important to use faster interfaces towards the spine than towards hosts to avoid congestion resulting from large/fat/elephant flows
   largest_potential_flow_size = 0
   def __init__(self, rack_dict):
      for attribute in self.required_attributes:
         if not rack_dict.has_key(attribute):
            util.log_error_and_exit(attribute+" is a mandatory variable and is missing from the provided configuration file")         
      for key, value in rack_dict.items():
         setattr(self, key, value)  
    
      try:
         self.rack_count = int(rack_dict["rack_count"])
      except ValueError:
         util.log_error_and_exit("Invalid value found for rack count for rack "+str(self.name)+" in provided fabric configuration")
 
      rack_host_networking =  Host_networking(self.host_network_interfaces,self.name)
      for nic in self.host_network_interfaces:
         ###Sum the total required host network capacity in the rack
         self.total_required_host_network_capacity += nic['speed'] * nic['count']
         ###Determine the fastest host facing interface speed in the rack
         if nic['speed'] > self.largest_potential_flow_size:
            self.largest_potential_flow_size = nic['speed']

      self.rack_host_networking = Host_networking(self.host_network_interfaces, self.name)
      self.total_required_fabric_network_capacity = math.ceil(util.calculate_sub_ratio(self.subscription_ratio_to_fabric) * self.total_required_host_network_capacity)
      if(self.total_required_fabric_network_capacity < 0):
         util.log_error_and_exit("Oversubscription ratio for rack "+str(self.name)+" of "+str(self.subscription_ratio_to_fabric)+" is invalid")
      
      
      
      ###print "Interfaces needed: "+str(self.rack_host_networking.host_interfaces_total)
      ###print "Total fabric network capacity required: "+str(self.total_required_fabric_network_capacity)            
      ###print "Rack created with a total host network capacity requirement of "+str(self.total_required_host_network_capacity)+" gigabits"
      ###print "It is recommended that this rack use spine interfaces with a speed greater than "+str(self.largest_potential_flow_size)+ " gigabits"
