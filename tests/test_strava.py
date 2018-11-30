import pytest
from unittest import mock


def test_strava(client, db_instance):
    with mock.patch('apigateway.apigateway.views.strava.current_user') as mocked:
        mocked.id = 1
        with mock.patch('apigateway.apigateway.views.strava.celery_app') as mocked_celery:
            client.get('/fetch')
            assert mocked_celery.send_task.called
