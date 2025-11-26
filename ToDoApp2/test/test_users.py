from .utils import *
from ..routers.users import get_db,get_current_user
from fastapi import status

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_return_users(test_user):
    response=client.get('/user/user')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    user_data=data[0]
    assert user_data['username'] == 'Hiren08'
    assert user_data['email'] == 'hiren@gmail.com'
    assert user_data['first_name'] == 'Hiren'
    assert user_data['last_name'] == 'savaliya'
    assert user_data['role'] == 'admin'

def test_change_password_success(test_user):
    response=client.put('/user/password', json={ 'password': 'testpassword', 'new_password':'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert response.json() == {'deteil': 'error on password change'}

def test_change_password_invalid_current_password(test_user):
    response=client.put('/user/password',json={'password':'wrong_password','new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'error on password change'}