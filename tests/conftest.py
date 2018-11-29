from apigateway.apigateway.database import db
import pytest
from unittest.mock import patch
import functools


def login_required(func):
    @functools.wraps(func)
    def _login_required(*args, **kw):
        return func(*args, **kw)
    return _login_required


@pytest.fixture
def app():
    patch('apigateway.apigateway.auth.login_required', login_required).start()
    from apigateway.apigateway.app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/apigateway.apigateway_test.db'

    yield app


@pytest.fixture
def app_login_required():
    from apigateway.apigateway.app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/apigateway.apigateway_test.db'

    yield app
    # os.unlink('/tmp/apigateway.apigateway_test.db')


@pytest.fixture
def db_instance(app):
    db.init_app(app)
    db.create_all(app=app)

    with app.app_context():
        yield db


@pytest.fixture
def db_instance_login_required(app_login_required):
    db.init_app(app_login_required)
    db.create_all(app=app_login_required)

    with app_login_required.app_context():
        yield db


@pytest.fixture
def client(app):
    client = app.test_client()

    yield client


@pytest.fixture
def client_login_required(app_login_required):
    client = app_login_required.test_client()

    yield client