from flask import Blueprint, render_template, redirect, request, abort, url_for
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from stravalib import Client
from monolith.database import db, User
from monolith.forms import LoginForm
from monolith.request_utils import users_endpoint, put_request_retry
import requests


auth = Blueprint('auth', __name__)


@auth.route('/strava_auth')
@login_required
def _strava_auth():
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    strava_token = xc(client_id=auth.app.config['STRAVA_CLIENT_ID'],
                      client_secret=auth.app.config['STRAVA_CLIENT_SECRET'],
                      code=code)

    try:
        user_id = current_user.id
        params = {
            'id': user_id,
            'strava_token': strava_token
        }
        r = put_request_retry(users_endpoint(), user_id, body=params)
        code = r.status_code
        if code == 204:
            return redirect(url_for('home.index'))
        else:
            return abort(400)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)
    return redirect('/')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect('/')
    return render_template('login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')
