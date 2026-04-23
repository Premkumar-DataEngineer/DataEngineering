#the purpose of this file to create DB model
#the purpose of the import is we are going to create the models for teh  database.py file
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Column, Boolean

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Todo(Base):
    __tablename__ = 'todos'  # table name  inside our database
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))


