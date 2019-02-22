import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import LoginUser, Base, Content, Client

engine = create_engine('sqlite:///pinet_screens.db?check_same_thread=False')
Base.metadata.bind = engine
DBParent = sessionmaker(bind=engine)
db_session = DBParent()


def create_user(username, hash, salt):
    user = LoginUser(username=username, password_hash=hash, password_salt=salt)
    db_session.add(user)
    db_session.commit()


def get_login_user_from_username(username):
    user = db_session.query(LoginUser).filter(LoginUser.username == username).first()
    return user


def get_all_content():
    content = db_session.query(Content).all()
    return content


def get_all_browser_content():
    content = db_session.query(Content).filter(Content.browser).all()
    return content


def get_all_script_content():
    content = db_session.query(Content).filter(Content.script).all()
    return content


def create_content(content_name, browser=False, script=False, url=None, script_body=None):
    if db_session.query(Content).filter(Content.content_name == content_name).first():
        return False # Content already exists with this name
    # TODO : Fix scripts being saved without newlines
    new_content = Content(content_name=content_name, browser=browser, url=url, script=script, script_body=script_body)
    db_session.add(new_content)
    db_session.commit()
    return True


def get_all_clients():
    clients = db_session.query(Client).all()
    return clients


def create_client(mac_address, hostname, location, client_id=None):
    if not client_id and (db_session.query(Client).filter(Client.mac_address == mac_address).first() or db_session.query(Client).filter(Client.hostname == hostname).first()):
        return False

    if client_id:
        client = db_session.query(Client).filter(Client.client_id == client_id).first()
    else:
        client = Client()
        client.ldm_autologin = False
    client.mac_address = mac_address
    client.hostname = hostname
    client.location = location
    db_session.add(client)
    db_session.commit()
    return client.client_id


def update_client_content(client_id, content_id):
    client = db_session.query(Client).filter(Client.client_id == int(client_id)).first()
    client.content_id = content_id
    db_session.commit()


def get_content_from_id(content_id):
    content = db_session.query(Content).filter(Content.content_id == int(content_id)).first()
    return content


def remove_content_from_id(content_id):
    content = get_content_from_id(content_id)
    db_session.delete(content)
    db_session.commit()


def get_client_from_id(client_id):
    client = db_session.query(Client).filter(Client.client_id == int(client_id)).first()
    return client


def remove_client_from_id(client_id):
    client = get_client_from_id(client_id)
    db_session.delete(client)
    db_session.commit()


def update_ldm_autologin(client_id, ldm_autologin):
    client = get_client_from_id(client_id)
    client.ldm_autologin = ldm_autologin
    db_session.commit()


def get_login_user_from_id(user_id):
    login_user = db_session.query(LoginUser).filter(LoginUser.user_id == int(user_id)).first()
    return login_user


def get_all_users():
    users = db_session.query(LoginUser).all()
    return users


def update_client_check_in(client_id):
    client = get_client_from_id(client_id)
    client.last_checked_in = datetime.datetime.now()
    db_session.commit()