# Starta docker
# Sätt MONGO_URL (env) till docker container http://localhost:27017/

import os
import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError

@pytest.fixture
def connect_to_test_db():
    os.environ['MONGO_URL'] = 'mongodb://root:root@localhost:27017/'

def test_create_valid_user(connect_to_test_db):
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
    test_dao.delete(res['_id']['$oid'])
    expectNone = test_dao.findOne(res.get('_id')['$oid'])
    assert expectNone == None

def test_create_invalid_user_no_first_name(connect_to_test_db):
    test_dao = DAO('user')
    test_user = {
        'lastName': 'Aro',
        'email': 'aro@tv3.se'
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

def test_create_invalid_user_no_last_name(connect_to_test_db):
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
        'email': 'aro@tv3.se'
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError

def test_create_invalid_user_no_last_name(connect_to_test_db):
    test_dao = DAO('user')
    test_user = {
        'firstName': 'Hasse',
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_user)
    assert exc_info.type == WriteError
    
def test_create_user_not_unique(connect_to_test_db):
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

    test_dao.delete(res['_id']['$oid'])
    expectNone = test_dao.findOne(res.get('_id')['$oid'])
    assert expectNone == None
