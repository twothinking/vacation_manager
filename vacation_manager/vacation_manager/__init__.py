"""Init Vacation Manager"""

import datetime
# pylint: disable=ungrouped-imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_user import UserManager
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, roles_accepted, login_required
from flask_admin import AdminIndexView, BaseView, Admin, expose
from flask_marshmallow import Marshmallow
from flask_admin.menu import MenuLink

from config import Config

# pylint: disable=invalid-name
app = Flask(__name__)
ma = Marshmallow(app)
login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)
db = SQLAlchemy(app)
app.config.from_object(Config)
migrate = Migrate(app, db)

# pylint: disable=wrong-import-position
from vacation_manager.models import User, Role, UserAvaliableVacationDays, AvaliableVacationDay, State


class MyAdminIndexView(AdminIndexView):
    """Admin index"""
    @expose('/')
    def index(self):
        if current_user.has_role("Admin"):
            return self.render('admin/index.html')
        return False

    def is_accessible(self):
        return current_user.has_role("Admin")


class MyView(BaseView):
    """My view"""
    @expose('/')
    def index(self):
        """Index"""
        if current_user.is_authenticated:
            return self.render('index.html')
        return False

    def is_accessible(self):
        return current_user.has_role("Admin")


class UserTools(ModelView):
    """User tools"""
    can_create = False
    can_delete = True
    page_size = 50
    column_list = ['email', 'active', 'roles']
    form_edit_rules = ['email', 'active', 'roles']
    column_searchable_list = ['email']


class VacationTools(ModelView):
    """Vacation Tools"""
    can_create = False
    can_delete = False
    column_searchable_list = [User.email, AvaliableVacationDay.avaliable_day, State.name]


admin = Admin(app, name="Vacation Manager", index_view=MyAdminIndexView())
admin.add_link(MenuLink(name='Home Page', url='/', category='Go To'))
admin.add_link(MenuLink(name='Logout', url='/logout', category='Go To'))
admin.add_view(UserTools(User, db.session))
admin.add_view(VacationTools(UserAvaliableVacationDays, db.session))

user_manager = UserManager(app, db, User)
# pylint: disable=wrong-import-position
from vacation_manager import routes, models
