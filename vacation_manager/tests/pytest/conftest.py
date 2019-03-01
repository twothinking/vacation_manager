import os
import tempfile

import pytest

from flask_security import SQLAlchemyUserDatastore


from vacation_manager import create_app, db
from vacation_manager.models import User, Role

USER_DATASTORE = SQLAlchemyUserDatastore(db, User, Role)


@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    return app


@pytest.fixture(scope='session')
def admin_user():
    user = User(email='admin_user@gmail.com', password='admin_pass', active=True)
    
    USER_DATASTORE.create_user(email=user.email, password=user.password, active=user.active)
    db.session.commit()

    USER_DATASTORE.add_role_to_user('admin_user@gmail.com', 'Admin')
    db.session.commit()

    return user


@pytest.fixture(scope='session')
def simple_user():
    user = User(email='simple_user@gmail.com', password='simple_pass', active=True)
    USER_DATASTORE.create_user(email=user.email, password=user.password, active=user.active)
    db.session.commit()
    USER_DATASTORE.add_role_to_user('simple_user@gmail.com', 'Employee')
    db.session.commit()

    return user