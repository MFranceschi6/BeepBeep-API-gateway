import pytest
from unittest import mock
from apigateway.apigateway.database import User
from requests.exceptions import RequestException


def test_create_user_no_connection(client, db_instance):
    with mock.patch('apigateway.apigateway.views.users.post_request_retry', side_effect=RequestException):
        res = client.post('/create_user', data={'password': 'p', 'email': 'gmat@mat.cio','firstname':'a', 'lastname': 'b',
                                     'age' : 2, 'weight': 2, 'max_hr': 20, 'rest_hr': 10, 'vo2max': 2.0})

    assert db_instance.session.query(User).count() == 0


def test_create_user_error(client, db_instance):
    with mock.patch('apigateway.apigateway.views.users.post_request_retry') as mocked:
        mocked.return_value.status_code = 400
        res = client.post('/create_user', data={'password': 'p', 'email': 'gmat@mat.cio', 'firstname': 'a', 'lastname': 'b',
                                                'age': 2, 'weight': 2, 'max_hr': 20, 'rest_hr': 10, 'vo2max': 2.0})

    assert db_instance.session.query(User).count() == 0


def test_create_user_wrong(client, db_instance):
    with mock.patch('apigateway.apigateway.views.users.post_request_retry') as mocked:
        mocked.return_value.status_code = 400
        res = client.post('/create_user', data={'passwd': 'p', 'email': 'gmat@mat.cio', 'firstname': 'a', 'lastname': 'b',
                                                'age': 2, 'weight': 2, 'max_hr': 20, 'rest_hr': 10, 'vo2max': 2.0})

    assert db_instance.session.query(User).count() == 0


def test_create_user(client, db_instance):
    with mock.patch('apigateway.apigateway.views.users.post_request_retry') as mocked:
        mocked.return_value.status_code = 204
        res = client.post('/create_user', data={'password': 'p', 'email': 'gmat@mat.cio', 'firstname': 'a', 'lastname': 'b',
                                                'age': 2, 'weight': 2, 'max_hr': 20, 'rest_hr': 10, 'vo2max': 2.0})
    print(res.data.decode('ascii'))
    assert db_instance.session.query(User).count() == 1


def test_remove_user_wrong_password(client, db_instance):
    user = User()
    user.set_email('example@example.com')
    user.set_password('password')
    db_instance.session.add(user)
    with mock.patch('apigateway.apigateway.views.users.current_user') as mocked:
        mocked.id = 1
        with mock.patch('apigateway.apigateway.views.users.try_delete_user') as mocker:
            client.post('/remove_user', data={'p': 'ciao'})

        assert not mocker.called


def test_remove_user_error(client, db_instance):
    user = User()
    user.set_email('example@example.com')
    user.set_password('password')
    db_instance.session.add(user)
    with mock.patch('apigateway.apigateway.views.users.current_user') as mocked:
        mocked.id = 1
        with mock.patch('apigateway.apigateway.views.users.delete_request_retry') as mocker:
            mocker.return_value.status_code = 400
            client.post('/remove_user', data={'password': 'password'})

    assert db_instance.session.query(User).count() == 1


def test_remove_user_no_connection(client, db_instance):
    user = User()
    user.set_email('example@example.com')
    user.set_password('password')
    db_instance.session.add(user)
    with mock.patch('apigateway.apigateway.views.users.current_user') as mocked:
        mocked.id = 1
        with mock.patch('apigateway.apigateway.views.users.delete_request_retry', side_effect=RequestException):
            client.post('/remove_user', data={'password': 'password'})

    assert db_instance.session.query(User).count() == 1


def test_remove_user_success(client, db_instance):
    user = User()
    user.set_email('example@example.com')
    user.set_password('password')
    db_instance.session.add(user)
    with mock.patch('apigateway.apigateway.views.users.current_user') as mocked:
        mocked.id = 1
        with mock.patch('apigateway.apigateway.views.users.delete_request_retry') as mocker:
            mocker.return_value.status_code = 204
            client.post('/remove_user', data={'password': 'password'})

    assert db_instance.session.query(User).count() == 0

