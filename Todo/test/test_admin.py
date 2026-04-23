from fastapi import status
from .utils import *
from ..router.admin import get_db, get_current_user

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_admin_read_all(test_todo):
    response=client.get("/admin/read_all/")
    print(response.url)
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code==status.HTTP_200_OK
    print(response.json())
    assert response.json() == [{'id': 1, 'title': 'Learning Fast API', 'priority': 1, 'owner_id': 1, 'description': 'Learn Python fastAPI using Udemy.', 'complete': False}]

