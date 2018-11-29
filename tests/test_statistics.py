from unittest import mock
from apigateway.apigateway.database import User
import pytest
#import datetime
from datetime import datetime
import requests




STATISTICS = 'apigateway.apigateway.views.statistics'


def correct_format_date(year=2025, month=2, day=1):
    return int(datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d').timestamp())


def test_view_statistics_invalid_login(client, db_instance):

    #try to test statistics without being logged in. Should yield an exception!
    with pytest.raises(Exception):
        client.get('/statistics', follow_redirects=True)





#Check and see if an exception is returned when the statistics webservice is down
def test_view_statistics_login_statistics_exception(client, db_instance):

    #firstly, mock the login
    with mock.patch(STATISTICS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        #now simulate the statistics being down
        with mock.patch(STATISTICS + '.get_request_retry', side_effect=Exception) as mocked:
            with pytest.raises(Exception):
                client.get('/statistics')

#Test and see if the statistics webservice could be found, but no run
def test_view_statistics_no_login_statistics_up(client, db_instance):

    with mock.patch(STATISTICS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        #now simulate the statistics microservice being up. Now, a a run is actually returned
        with mock.patch(STATISTICS + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 200

            #let's actually call the webservice now
            client_response = client.get('/statistics')

            assert client_response.status_code == 200


#Test and see if the statistics webservice couldn't be found
def test_view_statistics_no_login_statistics_not_found(client, db_instance):

    with mock.patch(STATISTICS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        #now simulate the statistics microservice being up. Now, a a run is actually returned
        with mock.patch(STATISTICS + '.get_request_retry') as mocked:
            mocked.return_value.status_code = 404

            #let's actually call the webservice now
            client_response = client.get('/statistics')

            assert client_response.status_code == 404


#Test and see if the statistics webservice is down
def test_view_statistics_no_login_statistics_down(client, db_instance):

    with mock.patch(STATISTICS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        #now simulate the statistics microservice being up. Now, a a run is actually returned
        with mock.patch(STATISTICS + '.get_request_retry', side_effect=requests.exceptions.RequestException) as mocked:
            mocked.return_value.status_code = 503
            client_response = client.get('/statistics')
            assert client_response.status_code == 503





#We actually need to try and login now!
def test_view_statistics_login_statistics_one_run(client, db_instance):

    #firstly, mock the login
    with mock.patch(STATISTICS + '.current_user') as current_user_mock:
        current_user_mock.id = 1
        #now simulate the statistics microservice being up. Now, a a run is actually returned
        with mock.patch(STATISTICS + '.get_request_retry') as mocked_runs:
            mocked_runs.return_value.status_code = 200

            mocked_runs.return_value.json.return_value = \
            {
                "distances" : [12],
                "average_speeds" : [14],
                "average_heart_rates" : [13],
                "elevation_gains": [11],
                "elapsed_times" : [13],
                "run_names" : ["corsa_al_parco"],
                "run_ids" : [1]
            }


            #let's actually call the webservice now
            client_response = client.get('/statistics')

            #print(client_response.data.decode('ascii'))

            assert client_response.status_code == 200


