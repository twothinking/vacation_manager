"""Configuration"""

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Config Object"""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sidefgsaofnaosihgfiuosabngfiuashfgasounfoassdg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
    SECURITY_PASSWORD_SALT = "csirkepaprikas"
    SECURITY_LOGIN_USER_TEMPLATE = 'custom/login.html'
    SECURITY_FLASH_MESSAGES = True
    