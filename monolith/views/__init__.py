from .home import home
from .auth import auth as _auth
from .users import users
# from .strava import strava
from .runs import runs
# from .training_objectives import training_objectives
# from .user_challenge import user_challenge
# from .statistics import statistics
from .profile import profile


blueprints = [home,
              _auth,
              users,
              # strava,
              runs,
              # training_objectives,
              # user_challenge,
              # statistics,
              profile,
              ]
