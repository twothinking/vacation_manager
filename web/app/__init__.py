from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_user import UserManager
import datetime
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, roles_accepted, login_required
from flask_admin import AdminIndexView, BaseView
from flask_marshmallow import Marshmallow
from flask_admin.menu import MenuLink

app = Flask(__name__)
ma = Marshmallow(app)
login = LoginManager(app)
login.login_view = 'login'
Bootstrap(app)
db = SQLAlchemy(app)
app.config.from_object(Config)
migrate = Migrate(app, db)

from app.models import User, Role, UserAvaliableVacationDays, AvaliableVacationDay, State

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.has_role("Admin"):
            return self.render('admin/index.html')
        abort(403)

    def is_accessible(self):
        return current_user.has_role("Admin")

class MyView(BaseView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return self.render('sindex.html')
        abort(403)

    def is_accessible(self):
        return current_user.has_role("Admin")

class UserTools(ModelView):
    can_create = False
    can_delete = True
    page_size = 50
    column_list = ['email','active','roles']
    form_edit_rules = ['email','active','roles']
    column_searchable_list = ['email']

class VacationTools(ModelView):
    can_create = False
    can_delete = False
    column_searchable_list = [User.email,AvaliableVacationDay.avaliable_day,State.name]

admin = Admin(app, name="Vacation Manager", index_view=MyAdminIndexView())
admin.add_link(MenuLink(name='Home Page', url='/', category='Go To'))
admin.add_link(MenuLink(name='Logout', url='/logout', category='Go To'))
admin.add_view(UserTools(User, db.session))
admin.add_view(VacationTools(UserAvaliableVacationDays, db.session))

user_manager = UserManager(app, db, User)

from app import routes, models
