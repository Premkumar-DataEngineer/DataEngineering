from .utils import *
from fastapi import status
from ..router.auth import get_current_user, get_db

app.dependency_overrides[get_db]=override_get_db
app.depenency_overrides[get_current_user]=override_get_current_user


