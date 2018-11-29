from unittest import mock
from requests.exceptions import RequestException

RUNS = 'apigateway.apigateway.views.runs'
GET_REQUEST_RETRY = RUNS + '.get_request_retry'
CURRENT_USER = RUNS + '.current_user'


def test_runs_abort_404(client, db_instance):
    user_id = 1
    run_id = 1
    with mock.patch(CURRENT_USER) as current_user_mock:
        current_user_mock.id = user_id
        with mock.patch(GET_REQUEST_RETRY) as request_mock:
            request_mock.return_value.status_code = 201

            result = client.get('/runs/{}'.format(run_id))
            assert result.status_code == 404


def test_runs_status_code_200(client, db_instance):
    user_id = 1
    run_id = 1
    with mock.patch(CURRENT_USER) as current_user_mock:
        current_user_mock.id = user_id
        with mock.patch(GET_REQUEST_RETRY) as request_mock:
            request_mock.return_value.status_code = 200
            request_mock.json = """{
               "average_heartrate":80.0,
               "average_speed":10.0,
               "description":"description",
               "distance":10.0,
               "elapsed_time":120,
               "id":1,
               "runner_id":2,
               "start_date":1543529477.483639,
               "strava_id":1,
               "title":"Run",
               "total_elevation_gain":2.0
            }"""

            result = client.get('/runs/{}'.format(run_id))
            assert result.status_code == 200


def test_runs_status_code_404(client, db_instance):
    user_id = 1
    run_id = 10
    with mock.patch(CURRENT_USER) as current_user_mock:
        with mock.patch(GET_REQUEST_RETRY) as request_mock:
            request_mock.return_value.status_code = 404
            current_user_mock.id = user_id
            result = client.get('/runs/{}'.format(run_id))
            assert result.status_code == 404


def test_runs_status_code_503(client, db_instance):
    user_id = 1
    run_id = 10
    with mock.patch(CURRENT_USER) as current_user_mock:
        with mock.patch(GET_REQUEST_RETRY,
                        side_effect=RequestException):

            current_user_mock.id = user_id
            result = client.get('/runs/{}'.format(run_id))
            assert result.status_code == 503


# def test_runs_login_required(client_login_required, db_instance_login_required):
#     result = client_login_required.get('/runs/1')
#     assert result.status_code == 302
