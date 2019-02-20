#!/usr/bin/env python3

import os
import time

import requests
import socket
import netifaces
import hashlib
from threading import Thread


server_address = "server" # Default LTSP IP address maps to server
script_root = "/usr/local/bin/scripts/"
file_hash = ""
ran_script_path = ""


def background_thread():
    time.sleep(30)
    while True:
        report_back(mac_address=get_mac_address())
        h = hash_file(ran_script_path)
        if h != file_hash:
            os.system("sudo reboot")
        time.sleep(60)


def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface.startswith("eth0") or interface.startswith("en"):
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
            return mac_address


def hash_file(path):
    global file_hash
    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()


def report_back(mac_address):
    r = requests.post("http://{}/endpoint/update".format(server_address), json={"mac_address":mac_address, "hostname":socket.getfqdn()})


def main():
    mac_address = get_mac_address()
    report_back(mac_address)
    thread = Thread(target=background_thread())
    thread.daemon = True
    thread.start()
    for file in os.listdir(script_root):
        if file == mac_address:
            print("Found match! {}".format(file))
            os.system("bash {}{}".format(script_root, file))

    thread.join()


if __name__ == '__main__':
    main()