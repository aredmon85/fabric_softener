import sys
import os
import ipaddress
import csv
import yaml
import util
import math
class Link:
   ###Used to represent the physical and logical connectivity between devices
   local_address = None
   local_form_factor = None
   remote_device = None
   remote_port = None
   remote_address = None
   remote_form_factor = None
   local_speed = None
   remote_speed = None
   subnet = None
   def __init__(self, local_device, local_port, local_form_factor, local_speed):
      self.local_device = local_device
      self.local_port = local_port
      self.local_form_factor = local_form_factor
      self.local_speed = local_speed
     
   def set_remote_vars(self, remote_device, remote_port, remote_form_factor, remote_speed):
      self.remote_device = remote_device
      self.remote_port = remote_port
      self.remote_form_factor = remote_form_factor
      self.remote_speed = remote_speed
 
