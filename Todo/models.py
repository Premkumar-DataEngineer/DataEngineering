#the purpose of this file to create DB model
#the purpose of the import is we are going to create the models for teh  database.py file
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Column, Boolean


class Todo(Base):
    __tablename__ = 'todos' # table name  inside our database
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

