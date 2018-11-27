from flask import Blueprint, render_template, request, abort, redirect, url_for
from apigateway.apigateway.auth import current_user, login_required
from apigateway.apigateway.request_utils import (challenges_endpoint,
                                                 get_request_retry,
                                                 post_request_retry)
import requests


challenges = Blueprint('challenges', __name__)

# def get_run(user_id, run_id):

#     try:
#         r = get_request(runs_endpoint(user_id), run_id)
#         code = r.status_code
#         if code == 200:
#             return r.json()

#     except requests.exceptions.RequestException as err:
#             print(err)
#             return abort(503)
#     return None


@challenges.route('/challenges/<id>', methods=['GET'])
@login_required
def create_challenge(id):

    try:

        user_id = current_user.id

        params = {'run_challenged_id': id}
        r = post_request_retry(challenges_endpoint(user_id), params=params)

        code = r.status_code
        if code == 204:
            return redirect(url_for('challenges.'))
        elif code == 404:
            return abort(code)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)

    return abort(400)


@challenges.route('/challenges', methods=['GET'])
@login_required
def _challenges():

    user_id = current_user.id

    if request.method == 'GET':

        try:
            r = get_request_retry(challenges_endpoint(user_id))

            code = r.status_code
            if code == 200:
                results = r.json()
                print(results)
                return render_template("challenges.html",
                                       results=results,
                                       challenge_id=None)
            elif code == 404:
                return abort(code)
        except requests.exceptions.RequestException as err:
            print(err)
            return abort(503)

    return abort(400)

    # if request.method == 'POST':
    #     id_run = request.form['id_run']
    #     current_run = db.session.query(Run).filter(Run.id == id_run).first()
    #     if current_run is not None:
    #         new_challenge = Challenge()
    #         new_challenge.challenged = current_run
    #         new_challenge.start_date = datetime.datetime.utcnow()
    #         new_challenge.runner = current_user
    #         db.session.add(new_challenge)
    #         db.session.commit()
    #         runs = db.session.query(Run).filter(Run.runner_id == new_challenge.runner_id).\
    #                         filter(Run.start_date > new_challenge.start_date)
    #         return render_template("challenges.html", challenge_id=new_challenge.id, runs=runs, run_challenged=current_run, run_challenger=None)
    # return redirect(url_for('home.index'))


# @user_challenge.route('/challenges/<id_challenge>')
# @login_required
# def _create_challenge(challenge_id):
#     current_challenge = db.session.query(Challenge).filter(Challenge.id == id_challenge).first()
#     try:
#         run_challenged = db.session.query(Run).filter(Run.id == current_challenge.run_challenged_id).first()
#     except AttributeError as e:
#         return redirect(url_for('home.index'))
#     if current_challenge.run_challenger_id is None:
#         runs = db.session.query(Run).filter(Run.runner_id == current_challenge.runner_id).\
#                         filter(Run.start_date > current_challenge.start_date)
#         return render_template("challenges.html", challenge_id=current_challenge.id, runs=runs, run_challenged=run_challenged, run_challenger=None)
#     else:
#         run_challenger = db.session.query(Run).filter(Run.id == current_challenge.run_challenger_id).first()
#         return render_template("challenges.html", challenge_id=current_challenge.id, run_challenged=run_challenged, run_challenger=run_challenger)

# @user_challenge.route('/terminate_challenge', methods=['GET','POST'])
# @login_required
# def terminate_challenge():
#     if request.method == 'POST':
#         id_challenger = request.form['id_challenger']
#         id_challenge = request.form['id_challenge']
#         current_challenge = db.session.query(Challenge).filter(Challenge.id == id_challenge).first()
#         current_run = db.session.query(Run).filter(Run.id == id_challenger).first()
#         if current_run is not None and current_challenge is not None:
#             if current_run.start_date > current_challenge.start_date:
#                 current_challenge.challenger = current_run
#                 current_challenge.result = determine_result(current_challenge, current_run)
#                 db.session.commit()
#                 return redirect(url_for('user_challenge.complete_challenge', id_challenge=id_challenge))
#     return redirect('/create_challenge')

# def determine_result(current_challenge, current_run):
#     challenged_run = db.session.query(Run).filter(Run.id == current_challenge.run_challenged_id).first()
#     if challenged_run.distance == current_run.distance:
#         return challenged_run.average_speed < current_run.average_speed
#     elif challenged_run.distance < current_run.distance:
#         return challenged_run.average_speed <= current_run.average_speed
#     else:
#         return False
