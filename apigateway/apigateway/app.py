import os
from werkzeug.exceptions import HTTPException
from flakon import create_app as _create_app
from flakon.util import error_handling
from apigateway.apigateway.views import blueprints
from apigateway.apigateway.auth import login_manager


_HERE = os.path.dirname(__file__)
os.environ['TESTDIR'] = os.path.join(_HERE, 'tests')
_SETTINGS = os.path.join(_HERE, 'settings.ini')


def create_app(settings=None):  # pragma: no cover
    if settings is None:
        settings = _SETTINGS

    template_folder = os.path.join(_HERE, 'templates')
    static_folder = os.path.join(_HERE, 'static')
    app = _create_app(blueprints=blueprints,
                      settings=settings,
                      template_folder=template_folder,
                      static_folder=static_folder)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']

    login_manager.init_app(app)

    return app


def create_testing_app():

    settings = _SETTINGS
    template_folder = os.path.join(_HERE, 'templates')
    static_folder = os.path.join(_HERE, 'static')
    app = _create_app(blueprints=blueprints,
                      settings=settings,
                      template_folder=template_folder,
                      static_folder=static_folder)

    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']
    app.config['TESTING'] = True

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)

    return app


def _400(desc):
    exc = HTTPException()
    exc.code = 400
    exc.description = desc
    return error_handling(exc)
