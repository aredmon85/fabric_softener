import ipaddress
import sys
import yaml
import socket
import re

class ccolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAILURE = '\033[91m'
    ENDCOLOR = '\033[0m'

def load_yaml_config_file(config_file):
    with open(config_file, 'r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    return config

def printfailure(message):
    print ccolors.FAILURE + message + ccolors.ENDCOLOR
def printwarn(message):
    print ccolors.WARNING + message + ccolors.ENDCOLOR
def printok(message):
    print ccolors.OKGREEN + message + ccolors.ENDCOLOR

def log_error_and_exit(log_msg):
    ###Log to stderr and exit
    sys.stderr.write(ccolors.FAILURE + "ERROR: "+log_msg+"\n" + ccolors.ENDCOLOR)
    sys.exit(1)

def validate_fabric_config(fabric_config):
	return True	
