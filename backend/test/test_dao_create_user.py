import pytest
from src.util.dao import DAO
from bson.objectid import ObjectId
from pymongo.errors import WriteError
from utils import setup_teardown, types

def test_create_valid_user():
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'lastName': 'Aro',
        'email': 'aro@tv3.se' 
    }
    res = test_dao.create(test_user)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Hasse'
    assert res['lastName'] == 'Aro'
    assert res['email'] == 'aro@tv3.se'

def test_create_valid_user_with_optional():
    test_dao = DAO('user')
    task_object_id = ObjectId('666f6f2d6261722d71757578')
    test_user = {
        'firstName': 'Hasse',
        'lastName': 'Aro',
        'email': 'aro@tv3.se',
        'tasks': [task_object_id]
    }
    res = test_dao.create(test_user)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Hasse'
    assert res['lastName'] == 'Aro'
    assert res['email'] == 'aro@tv3.se'
    assert res['tasks'] == [{'$oid': '666f6f2d6261722d71757578'}]

def test_create_invalid_user_no_first_name():
    test_dao = DAO('user')
    test_user = {
        'lastName': 'Aro',
        'email': 'aro@tv3.se'
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

def test_create_invalid_user_no_last_name():
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'email': 'aro@tv3.se'
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

def test_create_invalid_user_no_last_name():
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError
    
def test_create_user_not_unique():
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'lastName': 'Aro',
        'email': 'aro@tv3.se'
    }
    res = test_dao.create(test_user)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Hasse'
    assert res['lastName'] == 'Aro'
    assert res['email'] == 'aro@tv3.se'
    
    second_user = {
        'firstName': 'Hans',
        'lastName': 'Aroldsson',
        'email': 'aro@tv3.se'
    }

    with pytest.raises(Exception) as exc_info:
        test_dao.create(second_user)
    assert exc_info.type == WriteError

types_except_string = [item for item in types.items() if item[0] != 'string']

@pytest.mark.parametrize("_, value", types_except_string)
def test_firstName_invalid_types(_, value):
    test_dao = DAO('user')
    test_user = {
        'lastName': 'Aro',
        'email': 'aro@tv3.se'
    }
    test_user['firstName'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_string)
def test_lastName_invalid_types(_, value):
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'email': 'aro@tv3.se'
    }
    test_user['lastName'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_string)
def test_email_invalid_types(_, value):
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'lastName': 'Aro'
    }
    test_user['email'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

types_except_objectId = [item for item in types.items() if item[0] != 'objectId']

@pytest.mark.parametrize("_, value", types_except_objectId)
def test_tasks_invalid_types(_, value):
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'lastName': 'Aro',
        'email': 'aro@tv3.se'
    }
    test_user['tasks'] = [value]
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError
