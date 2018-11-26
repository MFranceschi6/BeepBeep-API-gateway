from flask_wtf import FlaskForm
import wtforms as f
import monolith.form_custom_models as fc
from wtforms.validators import DataRequired, NumberRange, Email
from monolith.form_custom_models import UniqueMailValidator
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),
                                            Email()])
    password = f.PasswordField('Password', validators=[DataRequired()])

    display = ['email',
               'password']


class RemoveUserForm(FlaskForm):
    password = f.PasswordField('Password', validators=[DataRequired()])

    display = ['password']


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),
                                            Email(),
                                            UniqueMailValidator()])
    firstname = f.StringField('Firstname', validators=[DataRequired()])
    lastname = f.StringField('Lastname', validators=[DataRequired()])
    password = f.PasswordField('Password', validators=[DataRequired()])
    age = f.IntegerField('Age', validators=[DataRequired()])
    weight = f.FloatField('Weight', validators=[DataRequired()])
    max_hr = f.IntegerField('Max Heartrate', validators=[DataRequired()])
    rest_hr = f.IntegerField('Rest Heartrate', validators=[DataRequired()])
    vo2max = f.FloatField('VO2 Max', validators=[DataRequired()])

    display = ['email',
               'firstname',
               'lastname',
               'password',
               'age',
               'weight',
               'max_hr',
               'rest_hr',
               'vo2max']


class ProfileForm(UserForm):
    email = EmailField('Email', validators=[DataRequired(),
                                            Email()])
    firstname = f.StringField('Firstname', validators=[DataRequired()])
    lastname = f.StringField('Lastname', validators=[DataRequired()])
    password = f.PasswordField('Password', validators=[])
    age = f.IntegerField('Age', validators=[DataRequired()])
    weight = f.FloatField('Weight', validators=[DataRequired()])
    max_hr = f.IntegerField('Max Heartrate', validators=[DataRequired()])
    rest_hr = f.IntegerField('Rest Heartrate', validators=[DataRequired()])
    vo2max = f.FloatField('VO2 Max', validators=[DataRequired()])
    periodicity = f.SelectField('Report Periodicity')

    display = ['email',
               'firstname',
               'lastname',
               'password',
               'age',
               'weight',
               'max_hr',
               'rest_hr',
               'vo2max',
               'periodicity']


class TrainingObjectiveSetterForm(FlaskForm):

    dateNotValid = 'Not a valid date'
    endNotValid = 'Cannot be before Start Date'
    kmNotValid = 'You need to run at least a meter'

    def kmFilter(value):
        if value is not None:
            return float('%.3f' % float(value))
        else:
            return value

    start_date = f.DateField('Start Date',
                             validators=[DataRequired(message=dateNotValid),
                                         fc.NotLessThenToday()],
                             widget=f.widgets.Input(input_type='date'))
    end_date = f.DateField('End Date',
                           validators=[DataRequired(message=dateNotValid),
                                       fc.NotLessThan('start_date',
                                                      message=endNotValid),
                                       fc.NotLessThenToday()],
                           widget=f.widgets.Input(input_type='date'))
    km_to_run = f.FloatField('Km to run',
                             validators=[DataRequired(kmNotValid),
                                         NumberRange(min=0.001,
                                         message=kmNotValid)],
                             widget=fc.FloatInput(step='any', min_='0'),
                             filters=[kmFilter])

    display = ['start_date',
               'end_date',
               'kilometers_to_run']


class TrainingObjectiveVisualizerForm(FlaskForm):
    start_date = f.DateField('Start Date')
    end_date = f.DateField('End Date')
    km_to_run = f.FloatField('Km to Run')
    traveled_kilometers = f.FloatField('Traveled Km')
    status = f.StringField('Status')
    description = f.StringField('Description')

    display = ['start_date',
               'end_date',
               'kilometers_to_run',
               'traveled_kilometers',
               'status',
               'description']
