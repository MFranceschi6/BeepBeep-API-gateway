from .home import home
from .auth import auth as _auth
from .users import users
from .strava import strava
from .runs import runs
# from .training_objectives import training_objectives
from .challenges import challenges
# from .statistics import statistics
from .profile import profile


blueprints = [home,
              _auth,
              users,
              strava,
              runs,
              # training_objectives,
              challenges,
              # statistics,
              profile,
              ]
