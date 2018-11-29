from unittest.mock import patch, Mock
from requests.exceptions import RequestException

HOME = 'apigateway.apigateway.views.home.'


def test_no_avarage_speed(client):
    with patch(HOME + 'Client') as mockedClient:
        mockedClient.return_value.authorization_url.return_value = 'fake_url'

        with patch(HOME + 'current_user') as mockedUser:
            mockedUser.id = 1

            with patch(HOME + 'get_request_retry') as mockGet:
                fake_response = mockGet.return_value
                fake_response.status_code = 400

                response = client.get('/')

                assert response.status_code == 400


def test_failed_first_get_request_retry(client):
    with patch(HOME + 'Client') as mockedClient:
        mockedClient.return_value.authorization_url.return_value = 'fake_url'

        with patch(HOME + 'current_user') as mockedUser:
            mockedUser.id = 1

            with patch(HOME + 'get_request_retry', side_effect=RequestException) as mockGet:

                response = client.get('/')

                assert response.status_code == 503


def test_failed_second_get_request_retry(client):
    with patch(HOME + 'Client') as mockedClient:
        mockedClient.return_value.authorization_url.return_value = 'fake_url'

        with patch(HOME + 'current_user') as mockedUser:
            mockedUser.id = 1

            def get_request_response_generator():
                fake_response = Mock().return_value
                fake_response.status_code = 200
                fake_response.json.return_value = dict(
                    average_speed=1
                )
                yield fake_response
                raise RequestException()

            gen = get_request_response_generator()
            def get_request_sideeffect(_, params):
                for x in gen:
                    return x

            with patch(HOME + 'get_request_retry', side_effect=get_request_sideeffect):
                response = client.get('/')
                assert response.status_code == 503



def test_failed_second_get_request_retry_404(client):
    with patch(HOME + 'Client') as mockedClient:
        mockedClient.return_value.authorization_url.return_value = 'fake_url'

        with patch(HOME + 'current_user') as mockedUser:
            mockedUser.id = 1

            def get_request_response_generator():
                fake_response1 = Mock().return_value
                fake_response1.status_code = 200
                fake_response1.json.return_value = dict(
                    average_speed=1
                )
                fake_response2 = Mock().return_value
                fake_response2.status_code = 404
                fake_response2.json.return_value = dict()
                yield fake_response1
                yield fake_response2

            gen = get_request_response_generator()
            def get_request_sideeffect(_, params):
                for x in gen:
                    return x

            with patch(HOME + 'get_request_retry', side_effect=get_request_sideeffect):
                response = client.get('/')
                assert response.status_code == 404


def test_good_response(client):
    with patch(HOME + 'Client') as mockedClient:
        mockedClient.return_value.authorization_url.return_value = 'fake_url'

        with patch(HOME + 'current_user') as mockedUser:
            mockedUser.id = 1

            def get_request_response_generator():
                fake_response = Mock().return_value
                fake_response.status_code = 200
                fake_response.json.return_value = dict(
                    average_speed=1
                )
                yield fake_response
                yield fake_response

            gen = get_request_response_generator()
            def get_request_sideeffect(_, params):
                for x in gen:
                    return x

            with patch(HOME + 'get_request_retry', side_effect=get_request_sideeffect):
                response = client.get('/')
                assert response.status_code == 200
