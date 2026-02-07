from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
#Data base handler
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#DB session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#DB object creation to control the DB
Base = declarative_base()


