from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

#the below statement would create the database and tables
models.Base.metadata.create_all(bind=engine)