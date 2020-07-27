import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
from sku import Sku
class Platform_engine:
 
   sku_list = [] 
   def __init__(self, platform_data_dict):
      if not platform_data_dict.has_key('platforms'):
         util.log_error_and_exit("Platform data is missing high level 'platform' key")
      for sku in platform_data_dict['platforms']:
         self.sku_list.append(Sku(sku))

   def match_tor_to_rack_requirements(self, rack):
      candidate_skus = list(self.sku_list)
      for candidate_sku in candidate_skus:
         if candidate_sku.power_current != rack.power_current:
            candidate_skus.remove(candidate_sku)
         if candidate_sku.airflow_direction != rack.airflow_direction and candidate_sku in candidate_skus:
            candidate_skus.remove(candidate_sku)
         if candidate_sku.vxlan != rack.vxlan_required and candidate_sku in candidate_skus:
            candidate_skus.remove(candidate_sku)
         if candidate_sku.max_power_draw != rack.power_available_for_network and candidate_sku in candidate_skus:
            candidate_skus.remove(candidate_sku)
      for candidate_sku in candidate_skus:
         print candidate_sku.sku
