from jose import jwt, JWTError
from .utils import *
import sys
sys.path.append("/Users/navyadev/Documents/GitHub/DataEngineering/Todo")
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import status, HTTPException
from datetime import timedelta, datetime, timezone
import pytest

app.dependency_overrides[get_db]=override_get_db

def test_authenticate_user(test_user):
    db=TestingSessionLocal()
    authenticated_user=authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    print(authenticated_user.username)
    assert authenticated_user.username == test_user.username

    non_exist_user=authenticate_user('Kumar','testpassword', db)
    assert non_exist_user is False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'admin'
    expires_delta = timedelta(minutes=5)
    token = create_access_token(username, user_id, role, expires_delta)
    print(token)
    decoded_token=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(type(decoded_token))
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user():
    encode={'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user=await get_current_user(token)
    assert user['username'] == 'testuser'
    assert user['user_id'] == 1
    assert user['role'] == 'admin'

@pytest.mark.asyncio
async def test_get_current_user_fail():
    encode={'role':'user'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as exinfo:
        await get_current_user(token)
    # try:
    #     await get_current_user(token)
    # except pytest.raises(HTTPException) as exinfo:
    #     print(exinfo.value)
    assert exinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exinfo.value.detail == 'Invalid token'



