from .home import home as homeView
from .auth import auth as _authView
from .users import users as usersView
from .strava import strava as stravaView
from .runs import runs as runsView
from .training_objectives import training_objectives as training_objectivesView
from .challenges import challenges as challengesView
from .statistics import statistics as statisticsView
from .profile import profile as profileView


blueprints = [homeView,
              _authView,
              usersView,
              stravaView,
              runsView,
              training_objectivesView,
              challengesView,
              statisticsView,
              profileView,
              ]
