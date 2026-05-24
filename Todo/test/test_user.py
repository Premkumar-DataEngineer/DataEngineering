import sys
sys.path.append("/Users/navyadev/Documents/GitHub/DataEngineering/Todo")
from .utils import *
from routers.users import get_current_user, get_db
from fastapi import status



app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_get_users(test_user):
    response = client.get("/user/")
    assert response.status_code==status.HTTP_200_OK
    print(response.json())

def test_get_specific_user(test_user):
    response=client.get("/user/1")
    assert response.status_code==status.HTTP_200_OK
    print(response.json())
    assert response.json().get("username")=="Prem"

def test_update_password(test_user):
    response=client.put("/user/password", json={"password":"testpassword",
                                                "new_password":"newpassword"})
    assert response.status_code==status.HTTP_204_NO_CONTENT




