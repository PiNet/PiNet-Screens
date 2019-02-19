import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from flask_login import UserMixin

Base = declarative_base()
engine = create_engine('sqlite:///pinet_screens.db')


class LoginUser(UserMixin, Base):

    def get_id(self):
        return self.user_id

    __tablename__= "login_users"
    user_id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    username = Column(String(30), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    password_salt = Column(String(100), nullable=False)


class Content(Base):
    __tablename__ = "content"
    content_id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    content_name = Column(String(30), nullable=False, unique=True)
    browser = Column(Boolean, nullable=False)
    url = Column(String(200), nullable=True)
    script = Column(Boolean, nullable=False)
    script_body = Column(String(2000), nullable=True)
    clients = relationship("Client")


class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    mac_address = Column(String(17), nullable=False, unique=True)
    hostname = Column(String(63), nullable=True, unique=True)
    location = Column(String(50), nullable=False)
    ldm_autologin = Column(Boolean, nullable=False)

    content_id = Column(ForeignKey('content.content_id'), primary_key=False, nullable=True, index=True)
    content = relationship('Content')


Base.metadata.create_all(engine)