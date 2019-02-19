from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import LoginUser, Base, Content

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
        return "Content already exists with this name"
    new_content = Content(content_name=content_name, browser=browser, url=url, script=script, script_body=script_body)
    db_session.add(new_content)
    db_session.commit()