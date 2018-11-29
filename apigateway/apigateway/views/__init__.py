from .home import home as _home
from .auth import auth as _auth
from .users import users as _users
from .strava import strava as _strava
from .runs import runs as _runs
from .training_objectives import training_objectives as _training_objectives
from .challenges import challenges as _challenges
from .statistics import statistics as _statistics
from .profile import profile as _profile


blueprints = [_home,
              _auth,
              _users,
              _strava,
              _runs,
              _training_objectives,
              _challenges,
              _statistics,
              _profile,
              ]
