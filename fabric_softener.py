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
	global_templatedir = global_localdir + "/templates"
	global_platform_data_file = global_localdir + "/data/platforms.yaml"
	
	if args.config and args.outdir:
		fabric_config = util.load_yaml_config_file(args.config)		
		util.validate_fabric_config(fabric_config)
		platform_data = util.load_yaml_config_file(global_platform_data_file)
		
		###User requirements
		###Determine the total number of hosts needing connectivity
		###the total number of interfaces and speeds of the interfaces for those hosts
		###and the total amount of host facing network capacity required.
		requirements = {}
		requirements['user_total_hosts'] = 0
                requirements['total_host_capacity'] = 0
                requirements['total_host_nic_sfp'] = 0
                requirements['total_host_nic_rj45_1G'] = 0
                requirements['total_host_nic_sfp+'] = 0
                requirements['total_host_nic_rj45_10G'] = 0
                requirements['total_host_nic_sfp28'] = 0
                requirements['total_host_nic_qsfp28'] = 0

                for host in fabric_config['fabric']['hosts']:
                        requirements['user_total_hosts'] += host['host_count']	
                        for nic in host['network_interfaces']:
				if nic['speed'] == 1 and nic['media'] == 'fiber':
					requirements['total_host_nic_sfp'] += host['host_count']	 
					requirements['total_host_capacity'] += 1 * host['host_count']
				elif nic['speed'] == 1 and nic['copper'] == 'copper':
					requirements['total_host_nic_rj45_1G'] += host['host_count']
					requirements['total_host_capacity'] += 1 * host['host_count']
				elif nic['speed'] == 10 and nic['media'] == 'fiber':
					requirements['total_host_nic_sfp+'] += host['host_count']
					requirements['total_host_capacity'] += 10 * host['host_count']
				elif nic['speed'] == 10 and nic['media'] == 'copper':
					requirements['total_host_nic_rj45_10G'] += host['host_count']
					requirements['total_host_capacity'] += 10 * host['host_count']
				elif nic['speed'] == 25:
					requirements['total_host_nic_sfp28'] += host['host_count']
					requirements['total_host_capacity'] += 25 * host['host_count']
				elif nic['speed'] == 50:
					requirements['total_host_nic_qsfp28'] += host['host_count']
					requirements['total_host_capacity'] += 50 * host['host_count']
				elif nic['speed'] == 100:
					requirements['total_host_nic_qsfp28'] += host['host_count']
					requirements['total_host_capacity'] += 100 * host['host_count']
		print "Total hosts: "+str(requirements['user_total_hosts'])
		print "Total host facing capacity required: "+str(requirements['total_host_capacity'])
		print "Total edge facing capacity required: "+str(fabric_config['fabric']['edge_facing_capacity'])
	else:
		parser.print_usage()
if __name__ == "__main__":
	main()
