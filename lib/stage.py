import argparse
import sys
import os
import csv
import yaml
import util
import math
from fabric_ports import Fabric_ports
from tor import Tor
from rack import Rack
from network_addressing import Network_addressing
class Stage:
   northbound_capacity = 0
   southbound_capacity = 0
   oversub_ratio = 1
   southbound_ports_list = None
   devices = []
   stage_id = 0 
   stage_speed = 0
   def __init__(self, stage_id, southbound_ports_list, oversub_ratio):
      self.stage_id = stage_id
      self.southbound_ports_list = southbound_ports_list
      self.oversub_ratio = oversub_ratio
      ###Take minimum sized approach
      ###Determine the minimum number of ports per device from the southbound stage - we ideally want to fully stripe the southbound against this stage.  
      ###e.g., if each southbound device has 4 ports, we need a minimum of 4 spine devices in this stage
      max_width = 16
      min_width = 0
      for fabric_port in southbound_ports_list:
         if len(fabric_port.ports_list) > min_width:
            min_width = len(fabric_port.ports_list)
         if len(fabric_port.ports_list) > max_width:
            ###We need to likely build a planar model
            util.log_error_and_exit("Planar design needed")
      if min_width % 4 == 0:
         print "Building stage "+str(stage_id)+" with a width of "+str(min_width) 
