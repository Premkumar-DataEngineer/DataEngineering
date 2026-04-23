from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, Path, APIRouter
from starlette import status
from .todo import get_db
from ..models import Todo, User
from .auth import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)
db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

@router.get("/read_all", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,
                   db:db_dependency
                   ):
    if user is None or user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(Todo).all()

@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(user:user_dependency,
                    db:db_dependency):
    if user is None or user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return db.query(User).all()