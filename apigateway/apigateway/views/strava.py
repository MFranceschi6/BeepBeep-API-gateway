import os
from celery import Celery
from flask import Blueprint, redirect
from apigateway.apigateway.auth import login_required

strava = Blueprint('strava', __name__)


BACKEND = BROKER = 'redis://' + os.environ[
    'REDIS'] + ":6379" if 'REDIS' in os.environ else "redis://127.0.0.1:6379"
celery_app = Celery(__name__, backend=BACKEND, broker=BROKER)


@strava.route('/fetch')
# @strava_token_required
@login_required
def fetch():
    # celery_app.send_task('fetch_all_runs')
    celery_app.send_task('datapump.datapump.periodic_fetch')
    return redirect('/')
    # res = fetch_runs_for_user.delay(current_user.id)
    # res.wait()
    # print(request.referrer)
    # if request.referrer is not None and 'login' not in request.referrer:
    #     return redirect(request.referrer)
    # return redirect('/')