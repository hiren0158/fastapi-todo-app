from ToDoApp2.test.test_example import test_list
from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from ..Database import Base
from sqlalchemy.orm import sessionmaker
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todos, Users
from ..routers.auth import bcrypt_context
import pytest

SQLALCHEMY_DATABASE_URL='sqlite:///./testdb.db'

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False},poolclass=StaticPool)

TestSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestSessionLocal()
    try:   
      yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'hiren','id':1,'user_role':'admin'}

client=TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(
        title='learn to code!',
        description='need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1,
    )
    db=TestSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('delete from todos2;'))
        connection.commit()

@pytest.fixture
def test_user():
    user=Users(
        username = 'Hiren08',
        email = 'hiren@gmail.com',
        first_name='Hiren',
        last_name='savaliya',
        hashed_password = bcrypt_context.hash('testpassword'),
        role = 'admin',
        # phone_number='9998887776'
    )

    db = TestSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('delete from users;'))
        connection.commit()
