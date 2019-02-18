import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
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




Base.metadata.create_all(engine)