from flask import Blueprint, render_template, abort, redirect, url_for
from apigateway.apigateway.auth import current_user, login_required
from flakon.request_utils import (runs_endpoint, challenges_endpoint,
                                  get_request_retry, post_request_retry,
                                  put_request_retry)
import requests
from datetime import datetime


challenges = Blueprint('challenges', __name__)


def get_run(run_id):
    if run_id is not None:
        user_id = current_user.id
        try:
            r = get_request_retry(runs_endpoint(user_id), run_id)
            code = r.status_code
            if code == 200:
                result = r.json()
                start_date = datetime.fromtimestamp(result['start_date'])
                result['start_date'] = start_date.strftime('%d/%m/%y at %H:%M')
                return result

        except requests.exceptions.RequestException as err:
                print(err)
    return None


def get_run_name(run_id):

    run = get_run(run_id)
    if run is not None:
        return run['title']
    return ""


@challenges.route('/challenges/<id>', methods=['GET'])
@login_required
def challenge_create(id):

    try:
        user_id = current_user.id
        params = {'run_challenged_id': int(id)}
        r = post_request_retry(challenges_endpoint(user_id), params=params)

        code = r.status_code
        if code == 200:
            result = r.json()
            challenge_id = result
            return redirect(url_for('challenges.challenge', id=challenge_id))
        else:
            return abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(400)


@challenges.route('/challenges', methods=['GET'])
@login_required
def _challenges():

    try:
        user_id = current_user.id
        r = get_request_retry(challenges_endpoint(user_id))

        code = r.status_code
        if code == 200:
            results = r.json()

            for r in results:

                run_challenged_id = r['run_challenged_id']
                run_challenger_id = r['run_challenger_id']
                start_date = datetime.fromtimestamp(r['start_date'])
                r['start_date'] = start_date.strftime('%d/%m/%y at %H:%M')

                r['run_challenged_name'] = get_run_name(run_challenged_id)
                r['run_challenger_name'] = get_run_name(run_challenger_id)

            return render_template("challenges.html",
                                   results=results,
                                   challenge_id=None)
        else:
            abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(400)


@challenges.route('/challenge/<id>', methods=['GET'])
@login_required
def challenge(id):

    try:
        user_id = current_user.id
        r = get_request_retry(challenges_endpoint(user_id), id)

        code = r.status_code
        if code == 200:

            challenged_run = None
            challenger_run = None
            runs = None
            won = False

            result = r.json()

            run_challenged_id = result['run_challenged_id']
            run_challenger_id = result['run_challenger_id']
            won = result['result']

            challenged_run = get_run(run_challenged_id)
            challenger_run = get_run(run_challenger_id)

            if run_challenger_id is None:
                start_date = datetime.fromtimestamp(result['start_date'])
                start_date_param = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                params = {
                    'start-date': start_date_param
                }
                try:
                    r = get_request_retry(runs_endpoint(user_id),
                                          params=params)

                    code = r.status_code
                    if code == 200:
                        runs = r.json()
                    else:
                        return abort(code)
                except requests.exceptions.RequestException as err:
                    print(err)
                    return abort(503)

            return render_template("challenge.html",
                                   id=id,
                                   challenged_run=challenged_run,
                                   challenger_run=challenger_run,
                                   runs=runs,
                                   won=won)
        else:
            abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(400)


@challenges.route('/challenges/<id>/complete/<challenger_id>',
                  methods=['GET'])
@login_required
def challenge_complete(id, challenger_id):

    try:
        user_id = current_user.id
        body = {
            'run_challenger_id': int(challenger_id)
        }
        r = put_request_retry(challenges_endpoint(user_id), id, body=body)

        code = r.status_code
        if code == 200:
            return redirect(url_for('challenges.challenge', id=id))
        else:
            return abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)
    return abort(400)
