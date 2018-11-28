import os
from celery import Celery
from flask import Blueprint, redirect
from apigateway.apigateway.auth import (login_required, strava_token_required,
                                        current_user)


strava = Blueprint('strava', __name__)


BACKEND = BROKER = 'redis://' + os.environ['REDIS'] + ":6379" \
                   if 'REDIS' in os.environ else "redis://127.0.0.1:6379"
celery_app = Celery(__name__, backend=BACKEND, broker=BROKER)


@strava.route('/fetch')
@strava_token_required
@login_required
def fetch_new_runs():
    user_id = current_user.id
    result = celery_app.send_task('datapump.datapump.fetch_runs_for_user',
                                  user_id=user_id)

    result.wait()
    return redirect('/')
    # res = fetch_runs_for_user.delay(current_user.id)
    # res.wait()
    # print(request.referrer)
    # if request.referrer is not None and 'login' not in request.referrer:
    #     return redirect(request.referrer)
    # return redirect('/')
