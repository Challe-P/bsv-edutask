import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError
from utils import setup_teardown, types

def test_create_valid_todo():
    test_dao = DAO('todo')
    test_todo = {
        'description': 'Finish paper'   
    }
    res = test_dao.create(test_todo)
    assert isinstance(res, dict)
    assert res['description'] == 'Finish paper'

def test_create_valid_todo_with_optional():
    test_dao = DAO('todo')
    test_todo = {
        'description': 'Finish paper',
        'done': False
    }
    res = test_dao.create(test_todo)
    assert isinstance(res, dict)
    assert res['description'] == 'Finish paper'

def test_create_not_unique_todo():
    test_dao = DAO('todo')
    test_todo = {
        'description': 'Finish paper'   
    }
    res = test_dao.create(test_todo)
    assert isinstance(res, dict)
    assert res['description'] == 'Finish paper'
    
    second_todo = {
        'description': 'Finish paper'
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(second_todo)
    assert exc_info.type == WriteError

def test_create_todo_no_description():
    test_dao = DAO('todo')
    test_todo = {
        'done': True        
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_todo)
    assert exc_info.type == WriteError
    
types_except_string = [item for item in types.items() if item[0] != 'string']

@pytest.mark.parametrize("_, value", types_except_string)
def test_invalid_types_description(_, value):
    test_dao = DAO('todo')
    test_todo = {
        'description': value
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_todo)
    assert exc_info.type == WriteError

types_except_bool = [item for item in types.items() if item[0] != 'boolean']

@pytest.mark.parametrize("_, value", types_except_bool)
def test_invalid_types_done(_, value):
    test_dao = DAO('todo')
    test_todo = {
        'description': 'Important document',
        'done': value
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_todo)
    assert exc_info.type == WriteError
