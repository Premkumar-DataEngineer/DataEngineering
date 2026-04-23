from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, Path, APIRouter
from starlette import status

from ..models import Base
from ..database import engine, SessionLocal
from ..models import Todo
from .auth import get_current_user


router = APIRouter()

#the below statement would create the database and tables
# it would only run if the todos db does not exceed.
#models.Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)

# create DB dependencies
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title:str = Field(min_length =3)
    description:str = Field(min_length =3, max_length =100)
    priority:int = Field(gt=0, lt=16)
    complete:bool


@router.get("/")
async def read_all(user:user_dependency,
                   db:db_dependency): # Dependencies injection - depends on get_db
    return db.query(Todo).filter(user.get('id')== Todo.owner_id).all()

@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,
                    db:db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")
    todo_item=db.query(Todo).filter(Todo.owner_id==user.get('id')).filter(Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo_item

@router.post("/todos",status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db:db_dependency,
                      todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    todo_item=Todo(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_item)
    db.commit()

@router.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,
                      db:db_dependency,todo_request:TodoRequest,
                      todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    todo_item=db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail='Todo content not found')
    todo_item.title = todo_request.title
    todo_item.description = todo_request.description
    todo_item.priority = todo_request.priority
    todo_item.complete = todo_request.complete
    db.add(todo_item)
    db.commit()
    return todo_item
@router.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,
                      db:db_dependency,
                      todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    todo_item=db.query(Todo).filter(user.get('id')==Todo.owner_id).filter(Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404,detail='Todo content not found')
    db.delete(todo_item)
    db.commit()







