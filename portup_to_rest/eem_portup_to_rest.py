#! /usr/bin/env python
"""
Description:
This script gathers details about a recently "uped" interface and
POSTs to a REST API

Author: Hank Preston <hapresto@cisco.com>

Illustrate the following concepts:
- Python Script to run On-Box using Guest Shell
- Gather informaiton from local device
- Send data off box for processing
"""

import re
import requests
import urllib3

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

# REST Server details
url = "https://requestb.in/y9b0eqy9"
headers = {"Content-type": "application/json"}

def send_details(switch, port, mac):
    """
    Send details to a REST endpoint.
    """
    data = {
            "switch": switch,
            "port": port,
            "mac_address": mac
           }

    response = requests.post(url, headers = headers, json = data, verify=False)
    return response

def get_device_hostname():
    """
    Get the device hostname
    """
    url = "https://192.168.35.1/restconf/data/Cisco-IOS-XE-native:native/hostname"
    headers = {"Content-type": "application/yang-data+json", "Accept": "application/yang-data+json"}
    response = requests.get(url, headers = headers, auth = ("vagrant", "vagrant"))
    return response.json()["Cisco-IOS-XE-native:hostname"]


# *Oct  5 20:04:41.343: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up
def get_interface_info(syslog):
    """
    Retrieve details about the interface desired.
    """
    pattern = re.compile('.* Interface (.*), .* ')
    interface = pattern.match(syslog).group(1)
    print("Interface: {}".format(interface))



# Entry point for program
if __name__ == '__main__':
    # Setup Arg Parse for Command Line parameters
    import argparse
    parser = argparse.ArgumentParser()

    # Command Line Parameters for Source and Destination IP
    parser.add_argument("syslog", help = "Syslog Message")
    args = parser.parse_args()

    # print("Sent Arguement: {}".format(args.syslog))

    get_interface_info(args.syslog)

    send_details("switch1", "ethernet1/1", "0000.aaaa.bbbb")
