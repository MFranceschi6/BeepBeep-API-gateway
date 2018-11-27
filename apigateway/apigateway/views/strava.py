from flask import Blueprint, redirect
from apigateway.apigateway.auth import login_required

strava = Blueprint('strava', __name__)


@strava.route('/fetch')
# @strava_token_required
@login_required
def fetch():
    # celery_app.send_task('fetch_all_runs')
    return redirect('/')
    # res = fetch_runs_for_user.delay(current_user.id)
    # res.wait()
    # print(request.referrer)
    # if request.referrer is not None and 'login' not in request.referrer:
    #     return redirect(request.referrer)
    # return redirect('/')