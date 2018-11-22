from flask import Blueprint, redirect, render_template, request, url_for, abort
from monolith.forms import UserForm, RemoveUserForm
from monolith.database import db, User
from monolith.auth import current_user, login_required
from monolith.forms import UserForm
from monolith.views.auth import strava_deauth
import requests
import functools
import time


_DATA_SERVICE = "http://127.0.0.1:5002"
_USERS_ENDPOINT = _DATA_SERVICE + "/users"

users = Blueprint('users', __name__)


def retry_request(func, retries = 6):
    @functools.wraps(func)
    def _retry_request(*args, **kw):  
        count = 0
        t = 1
        res = None
        while res is None and count < retries - 1:
            count += 1
            try:
                res = func(*args, **kw)
            except Exception as e:
                pass

            time.sleep(t)
            t *= 2

        if count == retries - 1:
            res = func(*args, **kw)
        return res

    return _retry_request


@retry_request
def request_create_user(params):
    return requests.post(_USERS, json = params)


@retry_request
def request_delete_user(user_id):
    return requests.delete(_USERS + "/" + str(user_id))


def try_create_user(new_user, params):
    try:
        r = request_create_user(params)
        code = r.status_code
        if code == 204:
            return redirect(url_for('home.index'))
        else:
            return abort_create_user(new_user, 400)
    except requests.exceptions.RequestException as err:
        print(err)
        return abort_create_user(new_user, 503)


def try_delete_user(user):
    try:
        r = request_delete_user(user.get_id())
        code = r.status_code
        if code == 204:
            db.session.delete(user)
            db.session.commit()
            strava_deauth(user)
            return redirect(url_for('home.index'))
        else:
            return abort(400)
    except requests.exceptions.RequestException as err:
        print(err)        
        return abort(503)
    

@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


def abort_create_user(new_user, error_code):
    db.session.delete(new_user)
    db.session.commit()
    return abort(error_code)


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            new_user.set_email(form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()

            params = {"id":        new_user.get_id(),
                      "email":     new_user.get_email(),
                      "firstname": form.firstname.data,
                      "lastname":  form.lastname.data,
                      #"strava_token": "string",
                      "age":       form.age.data,
                      "weight":    form.weight.data,
                      "max_hr":    form.max_hr.data,
                      "rest_hr":   form.rest_hr.data,
                      "vo2max":    form.vo2max.data
                    }
            return try_create_user(new_user, params)

    return render_template('create_user.html', form = form)


@users.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    form = RemoveUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_id  = current_user.id
            password = form.data['password']
            
            user = db.session.query(User).filter(User.id == user_id).first()
            if user is not None and user.authenticate(password):
                return try_delete_user(user)     

    return render_template('remove_user.html', form=form)
