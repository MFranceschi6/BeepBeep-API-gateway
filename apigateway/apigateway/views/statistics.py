from flask import Blueprint, render_template, abort
from apigateway.apigateway.auth import current_user, login_required
from flakon.request_utils import statistics_endpoint, get_request_retry
import requests


statistics = Blueprint('statistics', __name__)


def concatenate_run_name_id(run_names, run_ids):
    run_names_concatenated = []
    for run_id, run_name in zip(run_ids, run_names):
        run_names_concatenated.append(str(run_id) + "_" + run_name)
    return run_names_concatenated


def check_values(values):
    for v in values:
        if float(v) > 0.0:
            return values
    return None


@statistics.route('/statistics', methods=['GET'])
@login_required
def _statistics():

    try:
        user_id = current_user.id
        r = get_request_retry(statistics_endpoint(user_id))

        code = r.status_code
        if code == 200:
            results = r.json()

            distances = check_values(results["distances"])
            average_speeds = check_values(results["average_speeds"])
            average_heart_rates = check_values(results["average_heart_rates"])
            elevation_gains = check_values(results["elevation_gains"])
            elapsed_times = check_values(results["elapsed_times"])
            run_names = results["run_names"]
            run_ids = results["run_ids"]
            run_names = concatenate_run_name_id(run_names, run_ids)

            return render_template("statistics.html",
                                   distances=distances,
                                   average_speeds=average_speeds,
                                   average_heart_rates=average_heart_rates,
                                   elevation_gains=elevation_gains,
                                   elapsed_times=elapsed_times,
                                   run_names=run_names)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(404)
