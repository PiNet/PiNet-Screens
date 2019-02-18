import re


def is_mac_address(mac_address):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()): # Check if is a MAC address
        if mac_address.lower().startswith("b8:27:eb"): # Check if is a Raspberry Pi
            return True

    return False