from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True)
    user = Column(String())
    hashpass = Column(String(120))

class Roles(Base):
    __tablename__ = 'app_roles'

    id = Column(Integer, primary_key=True)
    user = Column(String())
    roles = Column(String())