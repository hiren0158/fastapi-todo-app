import pytest

def test_equal_or_not_equal():
    assert 3==3

def test_is_instance():
    assert isinstance('this is a string',str)
    assert not isinstance('10',int)

def test_boolean():
    validated=True
    assert validated is True
    assert ('hello'=='word') is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not str)

def test_greater_then_and_less_then():
    assert 7 > 4
    assert 5 < 10

def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class student:
    def __init__(self,firstname:str,lastname:str,major:str,years:int):
        self.first_name=firstname
        self.last_name=lastname
        self.major=major
        self.years=years

@pytest.fixture
def default_emplyoee():
    return student('Yash', 'Vasani', 'Computer Science', 3)

def test_person_initialization(default_emplyoee):
    assert default_emplyoee.first_name == 'Yash', 'First name should be Yash'
    assert default_emplyoee.last_name == 'Vasani', 'last name should be Vasani'
    assert default_emplyoee.major == 'Computer Science'
    assert default_emplyoee.years == 3

