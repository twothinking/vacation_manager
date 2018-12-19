import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
	USER_ENABLE_EMAIL = True        # Enable email authentication
	USER_ENABLE_USERNAME = False    # Disable username authentication
	USER_EMAIL_SENDER_NAME = USER_APP_NAME
	USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
	# USER_LOGIN_TEMPLATE = "login.html"
	# USER_REGISTER_TEMPLATE = "register.html"
	SECURITY_PASSWORD_SALT = "csirkepaprikas"
	SECURITY_LOGIN_USER_TEMPLATE = 'custom/login.html'
	SECURITY_FLASH_MESSAGES = True


	