import util
from typing import List, Dict


class RaspberryPi():
    mac_address = ""
    hostname = ""
    location = ""
    user = ""
    password = ""
    ldm_autologin = ""
    parameters = None

    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.parameters = {}


class LtsConf():
    parameters = dict()
    raspberry_pis: List[RaspberryPi] = list()
    path = ""

    def __init__(self, path):
        self.path = path

    def parse_conf(self):
        with open(self.path, "r") as f:
            current_raspberry_pi = None
            mac_address = None
            for line in f:
                line = line.strip()
                if line.startswith("#") and not line.startswith("# location"):
                    continue  # Can be ignored, a comment
                elif "[default]" in line:
                    mac_address = None
                elif line.startswith("[") and "]" in line:
                    base_mac_address = line.split("[")[1].split("]")[0]
                    if util.is_mac_address(base_mac_address):
                        mac_address = base_mac_address
                        if current_raspberry_pi:
                            self.raspberry_pis.append(current_raspberry_pi)
                        current_raspberry_pi = RaspberryPi(mac_address=mac_address)
                elif line.startswith("# location = "):
                    value = line.split("=")[1].strip()
                    current_raspberry_pi.location = value
                elif "=" in line:
                    key = line.split("=")[0].strip().lower()
                    value = line.split("=")[1].strip()
                    if current_raspberry_pi:
                        if key == "hostname":
                            current_raspberry_pi.hostname = value
                        elif key == "ldm_username":
                            current_raspberry_pi.user = value
                        elif key == "ldm_password":
                            current_raspberry_pi.password = value
                        elif key == "ldm_autologin":
                            current_raspberry_pi.ldm_autologin = value
                        else:
                            current_raspberry_pi.parameters[key] = value
                    else:
                        self.parameters[key] = value
                else:
                    print("Unknown line {}".format(line))

        if current_raspberry_pi:
            self.raspberry_pis.append(current_raspberry_pi)
        print("Done")

    def write_conf(self):
        conf_string = " # Generated by PiNet Screens. Editing this file by hand is not recommended.\n\n"
        for key, value in self.parameters.items():
            conf_string = conf_string + "{} = {}\n".format(key, value)

        for raspberry_pi in self.raspberry_pis:
            conf_string = conf_string + "\n[{}]\n".format(raspberry_pi.mac_address)
            if raspberry_pi.location:
                conf_string = conf_string + "   # location = {}\n".format(raspberry_pi.location)
            if raspberry_pi.hostname:
                conf_string = conf_string + "   hostname = {}\n".format(raspberry_pi.hostname)
            if raspberry_pi.ldm_autologin:
                conf_string = conf_string + "   ldm_autologin = True\n"
                conf_string = conf_string + "   ldm_username = {}\n".format(raspberry_pi.user)
                conf_string = conf_string + "   ldm_password = {}\n".format(raspberry_pi.password)
            for key, value in raspberry_pi.parameters.items():
                conf_string = conf_string + "   {} = {}\n".format(key, value)
        with open("test.conf", "w") as f:
            f.write(conf_string)