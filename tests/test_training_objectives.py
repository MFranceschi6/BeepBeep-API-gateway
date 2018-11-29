from unittest import mock
import requests
import re
from unittest.mock import patch

_TOS = 'apigateway.apigateway.views.training_objectives'
_FORMS = 'apigateway.apigateway.forms'

@patch(_TOS + '.current_user')
def test_get(current_user_mock, client, db_instance):
    current_user_mock.id = 1234567890

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


@patch(_TOS + '.current_user')
@patch(_TOS + '.TrainingObjectiveSetterForm')
def test_post(current_user_mock, setter_form_class_mock, client, db_instance):
    current_user_mock.id = 1234567890

    setter_form = setter_form_class_mock.return_value
    setter_form.validate_on_submit.return_value = True
    start_date = setter_form.start_data.data
    start_date.year = 2012
    start_date.month = 12
    start_date.day = 21
    end_date = setter_form.end_data.data
    end_date.year = 2012
    end_date.month = 12
    end_date.day = 23

    #RequestException captured
    with mock.patch(_TOS + '.post_request_retry') as mocked:
        mocked.side_effect = requests.exceptions.HTTPError(mock.Mock(status=404), 'not found')
        response = client.post('/training_objectives', follow_redirects=True)
    assert response.status_code == 503

    # status_code different from 201
    with mock.patch(_TOS + '.post_request_retry') as mocked:
        mocked.return_value.status_code = 404
        response = client.post('/training_objectives', follow_redirects=True)
    assert response.status_code == 404

    #working case
    with mock.patch(_TOS + '.post_request_retry') as mocked:
        mocked.return_value.status_code = 201
        with mock.patch(_TOS + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 201
            with mock.patch(_TOS + '.get_request_retry') as mocked:
                mocked.return_value.status_code = 200
                mocked.return_value.json.return_value = [
                    {
                        'start_date' : 123,
                        'end_date' : 234,
                        'kilometers_to_run' : 10.0,
                        'travelled_kilometers' : 13.33
                    }
                ]
                response = client.post('/training_objectives', follow_redirects=True)
    assert response.status_code == 200
    template = response.get_data(as_text=True)
    pattern = "^<html>(.|\n)*</html>$"
    assert re.match(pattern, template)
    pass
