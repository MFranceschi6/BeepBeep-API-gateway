from flask import Blueprint, render_template, abort
from apigateway.apigateway.auth import current_user, login_required
from flakon.request_utils import runs_endpoint, get_request_retry
from datetime import datetime
import requests


runs = Blueprint('runs', __name__)


@runs.route('/runs/<id>', methods=['GET'])
@login_required
def run(id):

    try:
        user_id = current_user.id
        r = get_request_retry(runs_endpoint(user_id), id)

        code = r.status_code
        if code == 200:
            run = r.json()

            run_id = run['id']
            name = run['title']
            timestamp = datetime.fromtimestamp(run['start_date'])
            date = timestamp.strftime('%A %d/%m/%y at %H:%M')
            headers = ['Distance (m)',
                       'AVG Speed (m/s)',
                       'Elapsed Time (s)',
                       'Elevation (m)']
            values = [run['distance'],
                      run['average_speed'],
                      run['elapsed_time'],
                      run['total_elevation_gain']]
            return render_template("runs.html",
                                   name=name,
                                   date=date,
                                   headers=headers,
                                   values=values,
                                   id=run_id)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(404)
