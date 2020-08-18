import argparse
import sys
import os
import csv
import yaml
import util
import math
from link import Link
from tor import Tor
from spine import Spine
from rack import Rack
from network_addressing import Network_addressing
class Stage:
   north_capacity = 0
   south_capacity = 0
   ###FIXME: May not be the best place for subscription ratio calculations - take another look
   oversub_ratio = 1
   south_links_list = []
   north_links_list = [] 
   devices = []
   unique_subordinate_devices = []
   stage_id = 0 
   stage_speed = 0
   stage_platform_links = []
   additional_stage_required = True

   links = []
   def __init__(self, stage_id, substage_links_list, platform_engine, edge_facing_capacity, oversub_ratio):
      self.stage_id = stage_id
      self.substage_links_list = substage_links_list
      self.oversub_ratio = oversub_ratio
      self.links = []
      ###Take minimum sized approach
      ###Determine the minimum number of links per device from the south stage - we ideally want to fully stripe the south against this stage.  
      ###e.g., if each south device has 4 links, we need a minimum of 4 spine devices in this stage
      max_width = 16
      min_width = 0
      if self.stage_id != 0:
         ###Identify all links flagged for connecting to this (the "next") stage and add them to the south_links_list
         for link in substage_links_list:
            if link.local_device not in self.unique_subordinate_devices:
               self.unique_subordinate_devices.append(link.local_device)
            if link.remote_device == "next_stage":
               self.south_links_list.append(link)
               self.south_capacity += link.remote_speed
               ###FIXME: Lazy way of setting the stage speed to the highest south facing link speed
               if self.stage_speed < link.remote_speed:
                  self.stage_speed = link.remote_speed
         ###Determine the width/planar dimensions of the stage 
         min_width = len(self.south_links_list) / len(self.unique_subordinate_devices)
         if min_width <= max_width:
            self.additional_stage_required = False
            ###FIXME: Not handling remainders here
            self.north_capacity = edge_facing_capacity
            north_link_count = math.ceil(edge_facing_capacity / self.stage_speed)
            for link in range(0,int(north_link_count)):
               ###FIXME: Edge facing capacity needs to be a class that captures the desired form factor of the connection
               self.north_links_list.append(Link(None,None,'QSFP28',100))
             
         ###We likely need to build a planar model
         ####util.log_error_and_exit("Planar design needed")

         ###Build the per spine link requirements
         for link in range(0,len(self.unique_subordinate_devices)):
            self.stage_platform_links.append(self.south_links_list[link])
         
         for link in range(0,int(north_link_count)):
            self.stage_platform_links.append(self.north_links_list[link]) 
        
         ###Build spine devices
         ###FIXME: Not matching SKU to environmental requirements for spines 
         sku = platform_engine.match_skus_to_link_reqs(self.stage_platform_links)
         for dev in range(0,min_width):
            self.devices.append(Spine(sku,self.stage_id,dev))

         spn_idx = 0
         spn_port_idx = 0
         for link in substage_links_list:
            if link.remote_device == "next_stage":
               link.remote_device = self.devices[spn_idx].name
               link.remote_speed = link.local_speed
               link.remote_form_factor = link.local_form_factor
               link.remote_port = self.devices[spn_idx].sku.ports.ports_list[spn_port_idx]['name']
               self.links.append(link) 
               spn_idx += 1
               if spn_idx == min_width:
                  spn_idx = 0   
                  spn_port_idx += 1
         if min_width % 4 == 0:
            print "Stage "+str(self.stage_id)+" created with a soutbound capacity of "+str(self.south_capacity)+" and width of "+str(min_width)

