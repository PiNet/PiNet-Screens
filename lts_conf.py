import util


class LtsConf():
    parameters = {}
    raspberry_pis = []
    path = None

    def __init__(self, path):
        self.path = path

    def parse_conf(self):
        with open(self.path,"r") as f:
            current_raspberry_pi = None
            mac_address = None
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue # Can be ignored, a comment
                elif "[default]" in line:
                    mac_address = None
                elif line.startswith("[") and "]" in line:
                    base_mac_address = line.split("[")[1].split("]")[0]
                    if util.is_mac_address(base_mac_address):
                        mac_address = base_mac_address
                        if current_raspberry_pi:
                            self.raspberry_pis.append(current_raspberry_pi)
                        current_raspberry_pi = RaspberryPi(mac_address=mac_address)
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


class RaspberryPi():
    mac_address = ""
    hostname = ""
    location = ""
    user = ""
    password = ""
    ldm_autologin = ""
    parameters = {}

    def __init__(self, mac_address):
        self.mac_address = mac_address
