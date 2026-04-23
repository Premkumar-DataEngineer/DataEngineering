from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.orm import Session
from ..models import User
from .auth import get_current_user
from ..database import SessionLocal

router=APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def get_users(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return db.query(User).filter(user.id == user.id).all()
