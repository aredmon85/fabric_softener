import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
from device import Device
class Spine(Device):
   def __init__(self, sku, stage_id, device_id):
      self.name = "t"+str(stage_id)+"_spn_"+str(device_id)
      self.sku = sku
      self.loopback_address = ""
      self.management_address = ""
      print "Spine Created with name: "+self.name
      #self.links = sku.ports.generate_spine_links(self.name, rack)
      #for link in self.links:
      #   print str(link.local_port+","+link.local_form_factor+","+str(link.local_speed)+","+link.remote_device+","+link.remote_port)       
