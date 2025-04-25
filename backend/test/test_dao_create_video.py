import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError
from utils import setup_teardown, types

def test_create_valid_video():
    test_dao = DAO('video')
    test_video = {
        'url': 'http://youtube.com/coolv1d3o/'        
    }
    res = test_dao.create(test_video)
    assert isinstance(res, dict)
    assert res['url'] == 'http://youtube.com/coolv1d3o/'

def test_create_video_no_url():
    test_dao = DAO('video')
    test_video = {
        'title': 'Video 1001'        
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_video)
    assert exc_info.type == WriteError
    
types_except_string = [item for item in types.items() if item[0] != 'string']

@pytest.mark.parametrize("_, value", types_except_string)
def test_invalid_types(_, value):
    test_dao = DAO('video')
    test_video = {
        'url': value
    }
    with pytest.raises(Exception) as exc_info:
        test_dao.create(test_video)
    assert exc_info.type == WriteError
