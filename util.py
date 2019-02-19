import re
import database
import flask_bcrypt
import random
import string


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
