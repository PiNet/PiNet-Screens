import re
import pinet_screens.database as database
import flask_bcrypt
import random
import string
import copy

import pinet_screens.lts_conf as lts_conf
import secrets.config
import os

default_new_client_message = """zenity --info --text '<span font="32">PiNet Screens</span><span font="20">\n\nThis client is not set up yet.\n\nHostname - {}\nMAC Address - {}</span>\n\n' --width 600"""

def is_mac_address(mac_address):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()): # Check if is a MAC address
        if mac_address.lower().startswith("b8:27:eb"): # Check if is a Raspberry Pi
            return True

    return False


def create_password_salt(password):
    salt = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    bcrypt_password = flask_bcrypt.generate_password_hash(password + salt)
    return salt, bcrypt_password


def validate_login(username, password):
    print("Attempting to validate login for {}".format(username))
    user = database.get_login_user_from_username(username)
    if user:
        if flask_bcrypt.check_password_hash(user.password_hash, password + user.password_salt):
            return True, user
    return False, None


def create_user(username, password):
    password_salt, password_hash = create_password_salt(password)
    database.create_user(username, password_hash, password_salt)


def write_browser(path, url):
    print("Writing browser to {} with {}".format(path, url))
    with open(path, "w") as f:
        f.write("chromium-browser --kiosk --app={}".format(url))


def write_script(path, script):
    print("Writing script to {} with {}".format(path, script))
    with open(path, "w") as f:
        f.write(script)





def build_scripts():
    clients = database.get_all_clients()
    lts = lts_conf.LtsConf(secrets.config.lts_conf_path)
    lts.old_raspberry_pis = copy.deepcopy(lts.raspberry_pis)
    lts.raspberry_pis = []
    for client in clients:
        new_client = lts_conf.RaspberryPi(mac_address=client.mac_address)
        new_client.hostname = client.hostname
        new_client.ldm_autologin = client.ldm_autologin
        new_client.user = secrets.config.default_pinet_username
        new_client.password = secrets.config.default_pinet_password
        new_client.location = client.location
        new_client.content = client.content
        for old_client in lts.old_raspberry_pis:
            if old_client.mac_address == new_client.mac_address:
                new_client.parameters = old_client.parameters
        lts.raspberry_pis.append(new_client)

    for old_client in lts.old_raspberry_pis:
        for new_client in lts.raspberry_pis:
            if old_client.mac_address == new_client.mac_address:
                break
        else:
            print("Old MAC address now found, adding {}".format(old_client.mac_address))
            #lts.raspberry_pis.append(old_client)
    print(lts.raspberry_pis)
    os.system("rm {}/*".format(secrets.config.client_config_files_path))
    lts.write_conf()

    for client in lts.raspberry_pis:
        if client.ldm_autologin:
            if client.content:
                if client.content.script:
                    write_script("{}/{}".format(secrets.config.client_config_files_path, client.mac_address), client.content.script_body)
                else:
                    write_browser("{}/{}".format(secrets.config.client_config_files_path, client.mac_address), client.content.url)
            else:
                write_script("{}/{}".format(secrets.config.client_config_files_path, client.mac_address), default_new_client_message.format(client.hostname, client.mac_address))






