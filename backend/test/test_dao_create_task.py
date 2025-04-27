import pytest
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from src.util.dao import DAO
from bson.objectid import ObjectId
from pymongo.errors import WriteError
from utils import setup_teardown, types


def test_create_valid_task():
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
        'description': 'Very important!'
    }
    res = test_dao.create(test_task)
    assert isinstance(res, dict)
    assert res['title'] == 'Important task!'
    assert res['description'] == 'Very important!'

def test_create_valid_task_with_optional():
    test_dao = DAO('task')
    task_object_array = [ObjectId('666f6f2d6261722d71757578')]
    categories = ['important', 'tasks']
    date = datetime.now()
    dueDate = datetime.now() + timedelta(days=10)
    todo_object_array = [ObjectId('666f6f2d6261722d71757580')]
    video_object_id = ObjectId('666f6f2d6261722d71757579')

    test_task = {
        'title': 'Important task!',
        'description': 'Very Important!',
        'startdate': date,
        'duedate': dueDate,
        'requires': task_object_array,
        'categories': categories,
        'todos': todo_object_array,
        'video': video_object_id
    }

    res = test_dao.create(test_task)
    assert isinstance(res, dict)
    assert res['title'] == 'Important task!'
    assert res['description'] == 'Very Important!'
    assert res['startdate'] == {'$date': f"{date.isoformat()[:-3]}Z"}
    assert res['duedate'] == {'$date': f"{dueDate.isoformat()[:-3]}Z"}
    assert res['requires'] == [{'$oid': '666f6f2d6261722d71757578'}]
    assert res['categories'] == categories
    assert res['todos'] == [{'$oid': '666f6f2d6261722d71757580'}]
    assert res['video'] == {'$oid': '666f6f2d6261722d71757579'}

def test_create_invalid_task_no_title():
    test_dao = DAO('task')
    test_task = {
        'description': 'Very Important!',
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

def test_create_task_not_unique():
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
        'description': 'Very Important!',
    }
    res = test_dao.create(test_task)
    assert isinstance(res, dict)
    assert res['title'] == 'Important task!'
    assert res['description'] == 'Very Important!'

    second_task = {
        'title': 'Important task!',
        'description': 'Not as important',
    }

    with pytest.raises(Exception) as exc_info:
        test_dao.create(second_task)
    assert exc_info.type == WriteError

types_except_string = [item for item in types.items() if item[0] != 'string']

@pytest.mark.parametrize("_, value", types_except_string)
def test_title_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': value
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_string)
def test_description_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['description'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_string)
def test_categories_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['categories'] = [value]
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

types_except_date = [item for item in types.items() if item[0] != 'date']

@pytest.mark.parametrize("_, value", types_except_date)
def test_startdate_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['startdate'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_date)
def test_duedate_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['duedate'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

types_except_objectId = [item for item in types.items() if item[0] != 'objectId']

@pytest.mark.parametrize("_, value", types_except_objectId)
def test_requires_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['requires'] = [value]
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_objectId)
def test_todos_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['todos'] = [value]
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError

@pytest.mark.parametrize("_, value", types_except_objectId)
def test_video_invalid_types(_, value):
    test_dao = DAO('task')
    test_task = {
        'title': 'Important task!',
    }
    test_task['video'] = value
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_task)
    assert exc_info.type == WriteError
