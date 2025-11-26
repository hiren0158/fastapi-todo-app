from .utils import *
from ..routers.admin import get_db,get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def read_admin_read_all_authenticated(test_todo):
    response=client.get
