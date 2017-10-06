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

# Localhost details
device_mgmt = "10.0.2.15"
device_user = "vagrant"
device_password = "vagrant"

# REST Server details
# Replace the IP with the IP of the server running the discovery api
discovery_server = "https://10.192.81.112"
headers = {"Content-type": "application/json"}

def send_details(switch, port, macs):
    """
    Send details to a REST endpoint.
    """
    url = discovery_server + "/api/discovery/link"
    data = {
            "switch": switch,
            "interface": port,
            "mac_addresses": macs
           }

    response = requests.post(url, headers = headers, json = data, verify=False)
    return response

def get_device_hostname():
    """
    Get the device hostname
    """
    url = "https://{}/restconf/data/Cisco-IOS-XE-native:native/hostname".format(device_mgmt)
    headers = {"Content-type": "application/yang-data+json",
               "Accept": "application/yang-data+json"
              }
    response = requests.get(url,
                            headers = headers,
                            auth = (device_user, device_password),
                            verify = False
                           )
    return response.json()["Cisco-IOS-XE-native:hostname"]



def get_interface_info(syslog):
    """
    Retrieve details about the interface desired.
    """
    # Sample syslog message:
    # *Oct  5 20:04:41.343: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to up
    pattern = re.compile('.* Interface (.*), .* ')
    interface = pattern.match(syslog).group(1)

    # Differences between L2 and L3 functions make the commands around mac
    # addresses different form Catalyst to IOS, providing placeholders for
    # actual mac address code that woudl be used on a Catalyst Switch
    mac_addresses = ["0000.aaaa.bbbb"]

    return {"interface": interface, "mac_addresses": mac_addresses}



# Entry point for program
if __name__ == '__main__':
    # Setup Arg Parse for Command Line parameters
    import argparse
    parser = argparse.ArgumentParser()

    # Command Line Parameters for Source and Destination IP
    parser.add_argument("syslog", help = "Syslog Message")
    args = parser.parse_args()

    interface_info = get_interface_info(args.syslog)
    hostname = get_device_hostname()

    send_details(hostname,
                 interface_info["interface"],
                 interface_info["mac_addresses"]
                )
