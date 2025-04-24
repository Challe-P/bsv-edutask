# Starta docker
# Sätt MONGO_URL (env) till docker container http://localhost:27017/

import os
import pytest
import json
from src.util.dao import DAO

@pytest.fixture
def connect_to_test_db():
    os.environ['MONGO_URL'] = 'mongodb://root:root@localhost:27017/'

def test_create(connect_to_test_db):
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
