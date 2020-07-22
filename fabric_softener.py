#!/usr/bin/env python
import argparse
import sys
import os
import csv
import yaml
import ipaddress
import lib.util as util
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
	global_templatedir = localdir + "/templates"
	global_platform_data_file = localdir + "/data/platforms.yaml"
	
	if args.config and args.outdir:
		fabric_config = util.load_yaml_config_file(args.config)		
		util.validate_fabric_config(fabric_config)
		platform_data = util.load_yaml_config_file(global_platform_data_file)
		

	else:
		parser.print_usage()
if __name__ == "__main__":
	main()
