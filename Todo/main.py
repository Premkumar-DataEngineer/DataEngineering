from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends


import models
from database import engine, SessionLocal
from models import Todo
app = FastAPI()

#the below statement would create the database and tables
# it would only run if the todos db does not exceed.
models.Base.metadata.create_all(bind=engine)

# create DB dependencies
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db:db_dependency): # Dependencies injection - depends on get_db
    return db.query(Todo).all()

