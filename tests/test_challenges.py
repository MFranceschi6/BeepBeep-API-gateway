import datetime
import requests
from unittest import mock
from werkzeug.exceptions import HTTPException

AUTH = 'apigateway.apigateway.auth'
CHALLENGES = 'apigateway.apigateway.views.challenges'


def test_challenges(client, db_instance):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 200    
            result = client.get('/challenges')

            print(result.json)
            assert result.status_code == 200

    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 404
            result = client.get('/challenges')

            print(result.json)
            assert result.status_code == 404

def test_challenge_create(client, db_instance):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.post_request_retry') as mocked:
            mocked.return_value.status_code = 200
            result = client.get('/challenges/1')

            print(result.json)
            assert result.status_code == 302
    
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.post_request_retry') as mocked:
            mocked.return_value.status_code = 404
            result = client.get('/challenges/1')

            print(result.json)
            assert result.status_code == 404

def test_challenge_complete(client, db_instance):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.put_request_retry') as mocked:
            mocked.return_value.status_code = 200
            result = client.get('/challenges/1/complete/1')
            assert result.status_code == 302

    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.put_request_retry') as mocked:
            mocked.return_value.status_code = 404
            result = client.get('/challenges/1/complete/1')
            assert result.status_code == 404
