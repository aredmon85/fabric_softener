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
   sku = None
   management_address = ""
   management_gateway = None
   loopback_address = "" 
   asn = None
   def __init__(self, sku, stage_id, device_id):
      self.name = "t"+stage_id+"_"+device_id
      self.sku = sku
      print "Device Created with name: "+self.name
