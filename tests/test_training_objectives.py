from unittest import mock
import requests
import re
from unittest.mock import patch

_TOS = 'apigateway.apigateway.views.training_objectives'

@patch(_TOS + '.current_user')
def test_get(current_user_mock, client, db_instance):
    current_user_mock.id = 123456

    #RequestException captured
    with mock.patch(_TOS + '.get_request_retry') as mocked:
        mocked.side_effect = requests.exceptions.HTTPError(mock.Mock(status=404), 'not found')
        response = client.get('/training_objectives', follow_redirects=True)
    assert response.status_code == 503

    #status_code different from 200
    with mock.patch(_TOS + '.get_request_retry') as mocked:
        mocked.return_value.status_code = 404
        response = client.get('/training_objectives', follow_redirects=True)
    assert response.status_code == 404

    #working case
    with mock.patch(_TOS + '.get_request_retry') as mocked:
        mocked.return_value.status_code = 200
        mocked.return_value.json.return_value = [
            {
                'start_date' : 1,
                'end_date' : 2,
                'kilometers_to_run' : 10.0,
                'travelled_kilometers' : 3.33
            },
            {
                'start_date' : 1,
                'end_date' : 2,
                'kilometers_to_run' : 10.0,
                'travelled_kilometers' : 5.5
            }
        ]
        response = client.get('/training_objectives', follow_redirects=True)
    assert response.status_code == 200
    template = response.get_data(as_text=True)
    pattern = "^<html>(.|\n)*</html>$"
    assert re.match(pattern, template)
    pass

