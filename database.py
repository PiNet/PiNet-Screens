from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import LoginUser, Base

engine = create_engine('sqlite:///pinet_screens.db')
Base.metadata.bind = engine
DBParent = sessionmaker(bind=engine)
db_session = DBParent()


def create_user(username, hash, salt):
    user = LoginUser(username=username, password_hash=hash, password_salt=salt)
    db_session.add(user)


def get_login_user_from_username(username):
    user = db_session.query(LoginUser).filter(LoginUser.username == username).first()
    return user