import datetime
import requests
from unittest import mock
from unittest.mock import Mock, MagicMock
from werkzeug.exceptions import HTTPException
from requests.exceptions import RequestException

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



def test_get_challenges_id_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.post_request_retry', side_effect=RequestException):
            result = client.get('/challenges/1')

            assert result.status_code == 503


def test_get_challenges_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.get_request_retry', side_effect=RequestException):
            result = client.get('/challenges')

            assert result.status_code == 503


def test_get_challenge_id_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.get_request_retry', side_effect=RequestException):
            result = client.get('/challenge/1')

            assert result.status_code == 503


def test_get_challenges_id_complete_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.put_request_retry', side_effect=RequestException):
            result = client.get('/challenges/1/complete/2')

            assert result.status_code == 503


def test_get_challenges_id_complete_bad_request(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.put_request_retry') as mocked:
            mocked.return_value.status_code = 404
            result = client.get('/challenges/1/complete/2')

            assert result.status_code == 404


def test_get_challenge_id_bad_request(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(CHALLENGES + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 404
            result = client.get('/challenge/1')

            assert result.status_code == 404


class AA:
    pass
    def json(self):
        return dict(
                start_date=1543536636
            )


def test_get_challenge_id(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1

        def get_request_response_generator():
            fake_response1 = Mock().return_value
            fake_response1.status_code = 200
            fake_response1.json.return_value = dict(
                run_challenged_id=1,
                run_challenger_id=2,
                result=True
            )

            fake_response2 = MagicMock().return_value
            fake_response2.status_code = 200
            fake_response2.json.return_value = dict(
                start_date=1543536636
            )
            fake_response3 = MagicMock().return_value
            fake_response3.status_code = 200
            fake_response3.json.return_value = dict(
                start_date=1543536636
            )

            yield fake_response1
            yield fake_response2
            yield fake_response3

        gen = get_request_response_generator()
        def get_request_sideeffect(_, params):
            for x in gen:
                return x

        with mock.patch(CHALLENGES + '.get_request_retry', side_effect=get_request_sideeffect):

            result = client.get('/challenge/1')

            assert result.status_code == 200



def test_get_challenge_id_None(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1

        def get_request_response_generator():
            fake_response1 = Mock().return_value
            fake_response1.status_code = 200
            fake_response1.json.return_value = dict(
                run_challenged_id=1,
                run_challenger_id=None,
                result=True,
                start_date=1543536636
            )

            fake_response2 = MagicMock().return_value
            fake_response2.status_code = 200
            fake_response2.json.return_value = dict(
                start_date=1543536636
            )
            fake_response3 = MagicMock().return_value
            fake_response3.status_code = 200
            fake_response3.json.return_value = [dict(
                start_date=1543536636
            )]

            yield fake_response1
            yield fake_response2
            yield fake_response3

        gen = get_request_response_generator()
        def get_request_sideeffect(_, params):
            for x in gen:
                return x

        with mock.patch(CHALLENGES + '.get_request_retry', side_effect=get_request_sideeffect):

            result = client.get('/challenge/1')

            assert result.status_code == 200



def test_get_challenge_id_None_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1

        def get_request_response_generator():
            fake_response1 = Mock().return_value
            fake_response1.status_code = 200
            fake_response1.json.return_value = dict(
                run_challenged_id=1,
                run_challenger_id=None,
                result=True,
                start_date=1543536636
            )

            fake_response2 = MagicMock().return_value
            fake_response2.status_code = 200
            fake_response2.json.return_value = dict(
                start_date=1543536636
            )
            fake_response3 = MagicMock().return_value
            fake_response3.status_code = 200
            fake_response3.json.return_value = [dict(
                start_date=1543536636
            )]

            yield fake_response1
            yield fake_response2
            raise RequestException

        gen = get_request_response_generator()
        def get_request_sideeffect(_, params):
            for x in gen:
                return x

        with mock.patch(CHALLENGES + '.get_request_retry', side_effect=get_request_sideeffect):

            result = client.get('/challenge/1')

            assert result.status_code == 503



def test_get_challenges_id_None_exception(client):
    with mock.patch(CHALLENGES + '.current_user') as current_user_mock:
        current_user_mock.id = 1

        with mock.patch(CHALLENGES + '.get_request_retry') as mocked:
            fake_response = mocked.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = [dict(
                start_date=1543536636,
                run_challenged_id=1,
                run_challenger_id=2
            )]

            with mock.patch(CHALLENGES + '.get_run') as mockedGetRun:
                mockedGetRun.return_value = None

                response = client.get('/challenges')

                assert response.status_code == 200
