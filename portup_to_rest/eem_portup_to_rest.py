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

import requests
import urllib3

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

# REST Server details
url = "https://requestb.in/1h99oul1"
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

# *Oct  5 20:04:41.343: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up
def get_interface_info():
    """
    Retrieve details about the interface desired.
    """

    return true


# Entry point for program
if __name__ == '__main__':
    # Setup Arg Parse for Command Line parameters
    import argparse
    parser = argparse.ArgumentParser()

    # Command Line Parameters for Source and Destination IP
    parser.add_argument("syslog", help = "Syslog Message")
    args = parser.parse_args()

    send_details("switch1", "ethernet1/1", "0000.aaaa.bbbb")
