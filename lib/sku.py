import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
class Sku:
   required_keys = [
      "sku",
      "airflow_direction",
      "power_current",
      "vxlan",
      "max_power_draw",
      "avg_power_draw",
      "recommended_software",
      "maximum_interfaces_per_port_group",
      "maximum_interfaces",
      "ports" ]

   def __init__(self, sku_dict):
      for key in self.required_keys:
         if not sku_dict.has_key(key):
            util.log_error_and_exit("SKU data is missing "+key+" for SKU: "+str(sku['sku'])) 
      for key, value in sku_dict.items():
         setattr(self, key, value)
