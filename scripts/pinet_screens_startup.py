#!/usr/bin/env python3

import os
import requests
import socket
import netifaces
server_address = "server" # Default LTSP IP address maps to server


def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface.startswith("eth0") or interface.startswith("en"):
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
            return mac_address


def report_back(mac_address):
    r = requests.post("http://{}/endpoint/update".format(server_address), json={"mac_address":mac_address, "hostname":socket.getfqdn()})


for interface in netifaces.interfaces():
    mac_address = get_mac_address()
    for file in os.listdir("scripts/"):
        if file == mac_address:
            print("Found match! {}".format(file))