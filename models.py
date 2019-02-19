import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('sqlite:///pinet_screens.db')


class LoginUser(Base):
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


Base.metadata.create_all(engine)