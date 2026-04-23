
from ..router.auth import get_current_user
from ..router.todo import get_db
from fastapi import status
from .utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_read_all_authenticated(test_todo):
    response=client.get("/")
    print('Response URL:',response.url)
    assert response.status_code==status.HTTP_200_OK
    print('Response data:',response.json())
    assert response.json()==[{'id': 1, 'priority': 1, 'owner_id': 1, 'complete': False, 'title': 'Learning Fast API', 'description': 'Learn Python fastAPI using Udemy.'}]

def test_read_one_authenticated(test_todo):
    response=client.get("/todos/1")
    print('Response URL:',response.url)
    assert response.status_code==status.HTTP_200_OK
    print('Response data:',response.json())
    assert response.json()=={'id': 1, 'priority': 1, 'owner_id': 1, 'complete': False, 'title': 'Learning Fast API', 'description': 'Learn Python fastAPI using Udemy.'}


def test_read_not_found_authenticated(test_todo):
    response=client.get("/todos/999")
    print('Response URL:',response.url)
    assert response.status_code==status.HTTP_404_NOT_FOUND
    print('Response data:',response.json())
    assert response.json()=={'detail':'Todo not found'}

def test_create_todo(test_todo):
    request_data={
        'title': 'Learning Polars API',
        'description': 'Learn Python Polars using Udemy.',
        'priority': 1,
        'complete': False,
    }
    response=client.post('/todos/',json=request_data)
    print('Response URL:',response.url)
    assert response.status_code==status.HTTP_201_CREATED
    db=TestingSessionLocal()
    model=db.query(Todo).filter(Todo.id==2).first()
    assert model.title==request_data['title']
    assert model.description==request_data['description']
    assert model.priority==request_data['priority']
    assert model.complete==request_data['complete']

def test_delete_todo(test_todo):
    db=TestingSessionLocal()
    model=db.query(Todo).filter(Todo.id==1).first()
    assert model.title==test_todo.title
    print(model.description)
    assert model.description==test_todo.description
    response=client.delete("/todos/1")
    print('Response URL:',response.url)
    assert response.status_code==status.HTTP_204_NO_CONTENT
    model=db.query(Todo).filter(Todo.id==1).first()
    assert model is None



