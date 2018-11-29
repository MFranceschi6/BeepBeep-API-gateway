from unittest import mock
from apigateway.apigateway.database import User
import pytest
import datetime

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

def test_one():
    assert 2==2