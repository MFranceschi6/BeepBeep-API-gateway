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
    print(celery_app)
    result = celery_app.send_task('datapump.datapump.fetch_runs_for_user',
                                  args=[user_id],
                                  queue="fetch")

    result.wait()
    return redirect('/')
