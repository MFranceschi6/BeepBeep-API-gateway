from flask import Blueprint, render_template, request, abort
from apigateway.apigateway.database import db
from apigateway.apigateway.auth import current_user, login_required
from apigateway.apigateway.forms import ProfileForm
from flakon.request_utils import (users_endpoint, get_request_retry,
                                  put_request_retry)
import requests
import enum


profile = Blueprint('profile', __name__)


class ReportPeriodicity(enum.Enum):
    No = 'No'
    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'


def get_modified_data(form):
    data = {}
    data['id'] = current_user.id
    data['email'] = form.email.data
    data['firstname'] = form.firstname.data
    data['lastname'] = form.lastname.data
    data['age'] = form.age.data
    data['weight'] = form.weight.data
    data['max_hr'] = form.max_hr.data
    data['rest_hr'] = form.rest_hr.data
    data['vo2max'] = form.vo2max.data
    data['report_periodicity'] = form.periodicity.data
    return data


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def _profile():

    user_id = current_user.id
    form = ProfileForm()
    form.periodicity.choices = [(p.name, p.value) for p in ReportPeriodicity]
    form.password.render_kw = {'placeholder': 'YOUR OLD PASSWORD'}

    if request.method == 'POST' and form.validate_on_submit():
        new_data = get_modified_data(form)
        if new_data is not {}:
            try:
                r = put_request_retry(users_endpoint(), user_id, new_data)
                code = r.status_code
                if code != 204:
                    return abort(code)
            except requests.exceptions.RequestException as err:
                print(err)
                return abort(503)

        new_password = form.password.data
        if new_password:
            current_user.set_password(new_password)
            db.session.commit()

    try:
        r = get_request_retry(users_endpoint(), user_id)

        code = r.status_code
        if code == 200:

            user = r.json()
            form.email.data = user['email']
            form.firstname.data = user['firstname']
            form.lastname.data = user['lastname']
            form.age.data = user['age']
            form.weight.data = user['weight']
            form.max_hr.data = user['max_hr']
            form.rest_hr.data = user['rest_hr']
            form.vo2max.data = user['vo2max']
            form.periodicity.data = user['report_periodicity']

            return render_template("profile.html", form=form)
        else:
            return abort(code)

    except requests.exceptions.RequestException as err:
        print(err)
        return abort(503)
