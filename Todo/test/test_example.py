import pytest

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

@pytest.fixture
def default_student():
    return Student('Prem', 40)

def testequalOrnotequal():
    assert 1 == 1
    assert 1 != 2

def testinstance():
    assert isinstance(1, int)
    assert isinstance('Prem', str)

def test_list():
    a=[1,2,3,4,5,6]
    assert 2 in a
    assert all(n>0 for n in a)
    assert any(n>3 for n in a)

def test_object(default_student):
    assert default_student.name == 'Prem'
    assert default_student.age == 40


