from unittest import mock

AUTH = 'apigateway.apigateway.auth'
RUNS = 'apigateway.apigateway.views.runs'


def test_runs(client, db_instance):
    with mock.patch(RUNS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        with mock.patch(RUNS + '.get_request_retry') as mocked:
            # Different from 200 to raise abort(404)
            mocked.return_value.status_code = 201

            result = client.get('/runs/1')
            assert result.status_code == 404


# # THIS TEST MUST FAIL BECOSE LOGIN_REQUIRED IS NOT MOKED
# def test_runs_login_required(client_login_required, db_instance_login_required):
#     with mock.patch(RUNS + '.current_user') as current_user_mock:
#         current_user_mock.id = 1
#         with mock.patch(RUNS + '.get_request_retry') as mocked:
#             mocked.return_value.status_code = 200

#             result = client_login_required.get('/runs/1')
#             assert result.status_code == 404
