import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
class Device:
   name = None
   links = []
   def __init__(self, sku, stage_id, device_id):
      self.name = "t"+stage_id+"_"+device_id
      print "Device Created with name: "+self.name
      #self.links = sku.ports.generate_tor_links(self.name, rack)
      #for link in self.links:
      #   print str(link.local_port+","+link.local_form_factor+","+str(link.local_speed)+","+link.remote_device+","+link.remote_port)       
