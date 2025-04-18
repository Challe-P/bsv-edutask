import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

def test_get_user_by_email_valid_unique():
    expected_result = {'id': 'user1', 'email': 'unique@test.com'}
    mocked_db = mock.MagicMock()
    mocked_db.find.return_value = [{'id': 'user1', 'email': 'unique@test.com'}]
    controller = UserController(dao=mocked_db)
    res = controller.get_user_by_email('unique@test.com')
    assert res == expected_result

def test_get_user_by_email_valid_not_unique(capfd):
    expected_result = {'id': 'user1', 'email': 'not_unique@test.com'}
    mocked_db = mock.MagicMock()
    mocked_db.find.return_value = [{'id': 'user1', 'email': 'not_unique@test.com'}, {'id': 'user2', 'email': 'not_unique@test.com'}]
    controller = UserController(dao=mocked_db)
    res = controller.get_user_by_email('not_unique@test.com')
    captured = capfd.readouterr()
    assert captured.out == 'Error: more than one user found with mail not_unique@test.com\n'
    assert res == expected_result

def test_get_user_by_email_valid_no_user():
    expected_result = None
    mocked_db = mock.MagicMock()
    mocked_db.find.return_value = []
    controller = UserController(dao=mocked_db)
    res = controller.get_user_by_email('unique@test.com')
    assert res == expected_result

def test_get_user_db_failure():
    mocked_db = mock.MagicMock()
    mocked_db.find = mock.Mock(side_effect=Exception)
    controller = UserController(dao=mocked_db)
    with pytest.raises(Exception) as exc_info:
        controller.get_user_by_email('unique@test.com')
    assert exc_info.type == Exception

@pytest.mark.parametrize('email', ['example@test.com', 'common.format@test.com', 'FirstName.LastName@TestTest.com', 
    'x@test.com', 'long-local-with-hyphens@and.subdomains.com', 'some.name+tag+tag@test.com',
    'sur/name@test.com', 'admin@test', '" "@test.com', '"very.(),:;<>[]\".VERY.\"very@\\ \"very\".strange"@unusual.test.com'])
def test_valid_email(email):
    expected_result = {'id': 'user1', 'email': email}
    mocked_db = mock.MagicMock()
    mocked_db.find.return_value = [{'id': 'user1', 'email': email}]
    controller = UserController(dao=mocked_db)
    res = controller.get_user_by_email(email)
    assert res == expected_result

@pytest.mark.parametrize('email', ['abc.test.com', 'a@b@c@test.com', '123', 't"o(o)s,p:e;c<i>a[l\k]l@test.com', 'no"quotes"allowed@test.com',
    'no spaces"and\quotes@test.com', 'even\ escaped\"chars\\arent@test.com', '1234567890123456789012345678901234567890123456789012345678901234+x@test.com',
    'no.underscores@are_allowed_here.com'])
def test_invalid_email(email):
    mocked_db = mock.MagicMock()
    controller = UserController(dao=mocked_db)
    with pytest.raises(ValueError) as exc_info:
        controller.get_user_by_email(email)
    assert exc_info.type == ValueError
