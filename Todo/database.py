from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#from sqlalchemy.ext.declarative import declarative_base

#SQLite DB
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
#PostgreSQL
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Prem1234!@localhost:5432/StudentDB'

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Data base connection handler
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
#DB session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#DB object creation to control the DB
Base = declarative_base()


