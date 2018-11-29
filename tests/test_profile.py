from unittest.mock import patch, Mock
from requests.exceptions import RequestException

PROFILE = 'apigateway.apigateway.views.profile.'


def test_get_request_bad_status_code(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            mockedGet.return_value.status_code = 404

            response = client.get('/profile')

            assert response.status_code == 404


def test_get_request_exception(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry', side_effect=RequestException):
            response = client.get('/profile')

            assert response.status_code == 503


def test_get_good_response(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            fake_response = mockedGet.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = dict(
                email='email',
                firstname='firstname',
                lastname='lastname',
                age='age',
                weight='weight',
                max_hr='max_hr',
                rest_hr='rest_hr',
                vo2max='vo2max',
                report_periodicity='report_periodicity',
            )

            response = client.get('/profile')

            assert response.status_code == 200


def test_post_put_bad_request(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            fake_response = mockedGet.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = dict(
                email='email',
                firstname='firstname',
                lastname='lastname',
                age='age',
                weight='weight',
                max_hr='max_hr',
                rest_hr='rest_hr',
                vo2max='vo2max',
                report_periodicity='report_periodicity',
            )

            with patch(PROFILE + 'ProfileForm') as mockedForm:
                mockedForm.return_value.validate_on_submit.return_value = True

                with patch(PROFILE + 'put_request_retry') as mockedPut:
                    put_response = mockedPut.return_value

                    put_response.status_code = 404

                    response = client.post('/profile')

                    assert response.status_code == 404


def test_post_put_exception(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            fake_response = mockedGet.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = dict(
                email='email',
                firstname='firstname',
                lastname='lastname',
                age='age',
                weight='weight',
                max_hr='max_hr',
                rest_hr='rest_hr',
                vo2max='vo2max',
                report_periodicity='report_periodicity',
            )

            with patch(PROFILE + 'ProfileForm') as mockedForm:
                mockedForm.return_value.validate_on_submit.return_value = True

                with patch(PROFILE + 'put_request_retry', side_effect=RequestException):   
                    response = client.post('/profile')

                    assert response.status_code == 503


def test_post_good_response_new_password_false(client):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            fake_response = mockedGet.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = dict(
                email='email',
                firstname='firstname',
                lastname='lastname',
                age='age',
                weight='weight',
                max_hr='max_hr',
                rest_hr='rest_hr',
                vo2max='vo2max',
                report_periodicity='report_periodicity',
            )

            with patch(PROFILE + 'ProfileForm') as mockedForm:
                fake_form = mockedForm.return_value
                fake_form.validate_on_submit.return_value = True

                fake_form.password.data = False

                with patch(PROFILE + 'put_request_retry') as mockedPut:
                    put_response = mockedPut.return_value

                    put_response.status_code = 204

                    response = client.post('/profile')

                    assert response.status_code == 200



def test_post_good_response(client, db_instance):
    with patch(PROFILE + 'current_user') as mockedUser:
        mockedUser.id = 1

        with patch(PROFILE + 'get_request_retry') as mockedGet:
            fake_response = mockedGet.return_value
            fake_response.status_code = 200
            fake_response.json.return_value = dict(
                email='email',
                firstname='firstname',
                lastname='lastname',
                age='age',
                weight='weight',
                max_hr='max_hr',
                rest_hr='rest_hr',
                vo2max='vo2max',
                report_periodicity='report_periodicity',
            )

            with patch(PROFILE + 'ProfileForm') as mockedForm:
                fake_form = mockedForm.return_value
                fake_form.validate_on_submit.return_value = True

                fake_form.password.data = True

                with patch(PROFILE + 'put_request_retry') as mockedPut:
                    put_response = mockedPut.return_value

                    put_response.status_code = 204

                    response = client.post('/profile')

                    assert response.status_code == 200
