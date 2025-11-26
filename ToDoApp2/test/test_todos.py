from ToDoApp2.test.test_main import client
from ..routers.todos import get_db,get_current_user
from starlette import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user


def test_read_all_authenticated(test_todo):
     response = client.get('/todos')
     assert response.status_code==status.HTTP_200_OK
     assert response.json() == [{'complete':False,'title':'learn to code!','description':'need to learn everyday!','priority':5,'id':1,'owner_id':1}] 

def test_read_one_authenticated(test_todo):
     response = client.get('/todos/todo/1')
     assert response.status_code==status.HTTP_200_OK
     assert response.json() == {'complete':False,'title':'learn to code!','description':'need to learn everyday!','priority':5,'id':1,'owner_id':1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get('todos//todos/999')
    assert response.status_code==404
    assert response.json() == {'detail': 'Not Found'}

def test_create_todo(test_todo):
    request_data={
        'title': 'new todo',
        'description':'new todo description',
        'priority':4,
        'complete':False,
    }

    response=client.post('/todos/todo',json=request_data)
    assert response.status_code == 201
    
    db=TestSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data={
        'title':'change the title of todo already saved!',
        'description':'Need to learn everyday',
        'priority':4,
        'complete':False,
    }

    response = client.put('/todos/todo/update_todo/1',json=request_data)
    assert response.status_code==204

    db=TestSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model.title == 'change the title of todo already saved!'

def test_update_todo_not_found(test_todo):
    request_data={
        'title':'change the title of todo already saved!',
        'description':'Need to learn everyday',
        'priority':4,
        'complete':False,
    }

    response = client.put('/todos/todo/update_todo/999',json=request_data)
    assert response.status_code==404

    db=TestSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert response.json()=={'detail':'todos not found'}

def test_delete_todo(test_todo):
    response=client.delete('todos/todo/delete-todo/1')
    assert response.status_code == 204
    db = TestSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None

def test_delete_todo_not_found():
    response=client.delete('todos/todo/delete-todo/999')
    assert response.status_code == 404
    assert response.json()=={'detail': 'todos not found'}