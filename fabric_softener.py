#!/usr/bin/env python
import argparse
import sys
import os
import csv
import yaml
import ipaddress
import lib.util as util
from lib.rack import Rack
from lib.fabric import Fabric
from lib.tor import Tor
from lib.platform_engine import Platform_engine
import json
from jinja2 import Environment, FileSystemLoader

def main():
   ###Command line arguments
   parser = argparse.ArgumentParser()
   parser.add_argument("--config", help="YAML file defining fabric configuration")
   parser.add_argument("--outdir", help="Output directory")
   args = parser.parse_args()

   ###Global variables
   global_localdir = os.path.dirname(os.path.realpath(__file__))
   global_templatedir = global_localdir + "/templates"
   global_platform_data_file = global_localdir + "/data/platforms.yaml"
   base_template = "base.tmpl"
   file_loader = FileSystemLoader(global_templatedir)
   env = Environment(loader=file_loader)
   config_template = env.get_template(base_template)
   
   if args.config and args.outdir:
      fabric_config = util.load_yaml_config_file(args.config)      
      util.validate_fabric_config(fabric_config)
      platform_data = util.load_yaml_config_file(global_platform_data_file)
      
      ###User requirements
      ###Determine the total number of racks needing connectivity
      ###the total number of interfaces and speeds of the interfaces for those racks
      ###and the total amount of rack facing network capacity required.
      platform_engine = Platform_engine(platform_data) 
      fabric = Fabric(fabric_config) 
      fabric_config = fabric.generate_fabric(platform_engine)
      for dev in fabric_config:
         print "Generating config for "+ dev['device'].name
         config_output = config_template.render(dev)
         util.write_file(config_output,dev['device'].name+".cfg",args.outdir)
   else:
      parser.print_usage()
if __name__ == "__main__":
   main()
