from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..models import Todo
from ..main import app

SQLALCHEMY_DATABASE_URI='sqlite:///./test.db'
engine=create_engine(SQLALCHEMY_DATABASE_URI,
                     connect_args={'check_same_thread': False},
                     poolclass=StaticPool)

TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'Prem', 'id': 1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo= Todo(
        title='Learning Fast API',
        description='Learn Python fastAPI using Udemy.',
        priority=1,
        complete=False,
        owner_id=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()