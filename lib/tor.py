import argparse
import sys
import os
import ipaddress
import csv
import yaml
import util
import math
class Tor:
   required_keys = [
      "model",
      "capacity",
      "skus",
      "vxlan",
      "max_power_draw",
      "avg_power_draw",
      "recommended_software" ]

   def __init__(self, platform_data_dict):
      for key in self.required_keys:
         if not platform_data_dict.has_key(key):
            util.log_error_and_exit("Platform data is missing "+key)
