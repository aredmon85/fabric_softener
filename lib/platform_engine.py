import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
import copy
from sku import Sku
class Platform_engine:
 
   sku_list = [] 
   def __init__(self, platform_data_dict):
      if not platform_data_dict.has_key('platforms'):
         util.log_error_and_exit("Platform data is missing high level 'platform' key")
      for sku in platform_data_dict['platforms']:
         self.sku_list.append(Sku(sku))

   def get_matching_tors_for_reqs(self, rack):
      valid_env_skus = self.match_tor_to_rack_environment_reqs(rack)
      valid_feature_skus = self.match_tor_to_feature_reqs(rack,valid_env_skus)
      valid_net_skus = self.match_tor_to_network_reqs(rack,valid_feature_skus)

   def match_tor_to_rack_environment_reqs(self, rack):
      candidate_skus = copy.deepcopy(self.sku_list)
      valid_skus = []
      skus_to_delete = []
      for idx in range(0,len(candidate_skus)):
         if candidate_skus[idx].power_current != rack.power_current:
            skus_to_delete.append(idx)
            continue
         if candidate_skus[idx].airflow_direction != rack.airflow_direction:
            skus_to_delete.append(idx)
            continue
         if candidate_skus[idx].max_power_draw > rack.power_available_for_network:
            skus_to_delete.append(idx)
            continue
      for idx in range(0,len(candidate_skus)):
         if idx not in skus_to_delete:
            valid_skus.append(candidate_skus[idx]) 
      return valid_skus

   def match_tor_to_network_reqs(self,rack,candidate_skus):
      valid_skus = []
      skus_to_delete = []
      for sku in candidate_skus:
         if sku.ports.can_support_port_requirements(rack):
            valid_skus.append(sku)
            print "SUCCESS: SKU "+sku.sku+" can support this rack"

   def match_tor_to_feature_reqs(self,rack,candidate_skus):
      valid_skus = []
      skus_to_delete = []
      if rack.vxlan_required == True:
         for idx in range(0,len(candidate_skus)):
            if candidate_skus[idx].vxlan != rack.vxlan_required:
               skus_to_delete.append(idx)
               continue
      for idx in range(0,len(candidate_skus)):
         if idx not in skus_to_delete:
            valid_skus.append(candidate_skus[idx])
      return valid_skus

