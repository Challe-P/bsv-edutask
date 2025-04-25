import os
import pytest
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

@pytest.fixture(autouse=True)
def setup_teardown():
    test_url = 'mongodb://root:root@localhost:7357/'
    os.environ['MONGO_URL'] = test_url

    yield
    client = pymongo.MongoClient(test_url)
    client.drop_database('edutask')

types = {
    'int': 1,
    'float': 1.20,
    'string': 'string',
    'boolean': True,
    'null': None,
    'date': datetime.now(),
    'objectId': ObjectId(),
    'timestamp': datetime.timestamp(datetime.now()),
    'array': [1, 2, 3],
    'object': {'key': 'value'}
    }
