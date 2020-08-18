import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
from device import Device
class Tor(Device):
   def __init__(self, rack, rack_id, sku):
      self.name = "t0_"+rack.name+"_"+str(rack_id)
      self.sku = sku
      self.loopback_address = ""
      self.management_address = ""
      print "TOR Created with name: "+self.name
      #self.links = sku.ports.generate_tor_links(self.name, rack)
      #for link in self.links:
      #   print str(link.local_port+","+link.local_form_factor+","+str(link.local_speed)+","+link.remote_device+","+link.remote_port)       
