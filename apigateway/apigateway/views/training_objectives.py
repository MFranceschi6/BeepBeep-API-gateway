from flask import Blueprint, render_template, request, abort
from flask_login import current_user
from apigateway.apigateway.auth import login_required
from apigateway.apigateway.forms import (TrainingObjectiveSetterForm,
                                         TrainingObjectiveVisualizerForm)
from flakon.request_utils import (objectives_endpoint, get_request_retry,
                                  post_request_retry)
import requests
from datetime import datetime, timezone


training_objectives = Blueprint('training_objectives', __name__)


def timestamp_to_date(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    return date.strftime('%d/%m/%y')


def timestamp_to_utc(timestamp):
    return datetime.utcfromtimestamp(timestamp)


def date_to_utc_timestamp(date):
    date_time = datetime(year=date.year,
                         month=date.month,
                         day=date.day)
    return date_time.replace(tzinfo=timezone.utc).timestamp()
    # return (date - datetime(1970, 1, 1)) / timedelta(seconds=1)


@training_objectives.route('/training_objectives', methods=['GET', 'POST'])
@login_required
def _training_objectives():

    user_id = current_user.id
    setter_form = TrainingObjectiveSetterForm()
    visualizer_form = TrainingObjectiveVisualizerForm()

    results = None

    if request.method == 'POST':
        if setter_form.validate_on_submit():

            start_date = date_to_utc_timestamp(setter_form.start_date.data)
            end_date = date_to_utc_timestamp(setter_form.end_date.data)
            km_to_run = setter_form.km_to_run.data

            params = {
                'start_date': start_date,
                'end_date': end_date,
                'kilometers_to_run': km_to_run
            }

            print(params)

            try:
                r = post_request_retry(objectives_endpoint(user_id),
                                       params=params)
                code = r.status_code
                if code != 201:
                    return abort(code)
            except requests.exceptions.RequestException as err:
                print(err)
                return abort(503)

    try:
        r = get_request_retry(objectives_endpoint(user_id))

        code = r.status_code
        if code == 200:
            results = r.json()

            now_utc = datetime.utcnow()

            for result in results:
                end_date_utc = timestamp_to_utc(result['end_date'])
                result['is_expired'] = end_date_utc < now_utc
                result['start_date'] = timestamp_to_date(result['start_date'])
                result['end_date'] = timestamp_to_date(result['end_date'])
                km_to_run = result['kilometers_to_run']
                travelled_kilometers = result['travelled_kilometers']
                result['km_left'] = km_to_run - travelled_kilometers
        else:
            return abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return render_template("training_objectives.html",
                           training_objectives_list=results,
                           setter_form=setter_form,
                           visualizer_form=visualizer_form)
