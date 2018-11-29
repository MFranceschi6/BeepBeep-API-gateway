from unittest import mock
from apigateway.apigateway.database import User
import pytest
import datetime
import functools

AUTH = 'apigateway.apigateway.auth'
RUNS = 'apigateway.apigateway.views.runs'


def login_required(func):
    @functools.wraps(func)
    def _login_required(*args, **kw):
        return func(*args, **kw)
    return _login_required

def make_and_login_user(client, db_instance):
    response = client.post('/create_user', follow_redirects=True, data=dict(
        submit='Publish',
        email='test@email.com',
        firstname='1',
        lastname='1',
        password='1',
        age='1',
        weight='1',
        max_hr='1',
        rest_hr='1',
        vo2max='1'))

    assert response.status_code == 200
    print(response.data.decode('ascii'))
    assert b'> Please Login or Register </' in response.data

    response = client.post('/login', follow_redirects=True, data=dict(email='test@email.com', password='1'))
    assert response.status_code == 200
    print(response.data.decode('ascii'))
    assert b'>Hi test@email.com </' in response.data


def test_runs(client, db_instance):
    with mock.patch(RUNS + '.login_required', login_required):
        with mock.patch(RUNS + '.current_user') as current_user_mock:
            current_user_mock.id = 1
            with mock.patch(RUNS + '.get_request_retry') as mocked:
                obj = mocked.return_value
                obj.status_code = 201

                result = client.get('/runs/1')
                assert result.status_code == 404
