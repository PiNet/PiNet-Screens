#!/usr/bin/env python3

import os
import requests
import socket
import netifaces
server_address = "server" # Default LTSP IP address maps to server


def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if "eth0" in  interface or "en" in interface:
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK]["addr"]
            return mac_address


def report_back(mac_address):
    r = requests.post("http://{}/endpoint/update".format(server_address), json={"mac_address":mac_address, "hostname":socket.getfqdn()})


for interface in os.walk("/sys/class/net/"):
    mac_address = get_mac_address()
    for file in os.listdir("scripts/"):
        if file == mac_address:
            print("Found match! {}".format(file))