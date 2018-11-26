from flask import Blueprint, render_template, abort
from stravalib import Client
from monolith.auth import current_user
from monolith.request_utils import (users_endpoint, runs_endpoint,
                                    get_request_retry)
import requests

home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


@home.route('/')
def index():

    average_speed = None
    strava_auth_url = _strava_auth_url(home.app.config)

    if current_user is not None and hasattr(current_user, 'id'):

        user_id = current_user.id

        # Average Speed
        try:
            r = get_request_retry(users_endpoint(user_id), 'average')
            code = r.status_code
            if code == 200:
                result = r.json()
                average_speed = result['average_speed']
            else:
                return abort(code)
        except requests.exceptions.RequestException as err:
            print(err)
            return abort(503)

        # Runs
        try:
            params = {
                'page': 0,
                "per_page": 10
            }
            print(runs_endpoint(user_id))

            r = get_request_retry(runs_endpoint(user_id), params=params)
            code = r.status_code
            if code == 200:
                result = r.json()
                print(result)
            else:
                return abort(code)
        except requests.exceptions.RequestException as err:
            print(err)
            return abort(503)

    print(average_speed)

    return render_template('index.html',
                           strava_auth_url=strava_auth_url,
                           average_speed=average_speed)
