"""Routes"""

import json
from datetime import datetime

from flask import render_template, url_for, request, flash, redirect
from flask_security import (
    Security, SQLAlchemyUserDatastore,
    login_required, utils,
    roles_accepted,
    logout_user, current_user)
from sqlalchemy import exists

from vacation_manager.forms import RegisterForm, ExtendedLoginForm
from vacation_manager.models import (
    User, Role, AvaliableVacationDay,
    AvaliableVacationDaySchema, State,
    UserAvaliableVacationDays)
from vacation_manager import app, db


# pylint: disable=no-member


USER_DATASTORE = SQLAlchemyUserDatastore(db, User, Role)
SECURITY = Security(app, USER_DATASTORE, login_form=ExtendedLoginForm)


@app.before_first_request
def before_first_request():
    """Insert before first request"""
    db.create_all()

    state_pending = State(name="Pending")
    state_accepted = State(name="Accepted")
    state_declined = State(name="Declined")

    if not db.session.query(exists().where(State.name == "Pending")).scalar():
        db.session.add(state_pending)
    if not db.session.query(exists().where(State.name == "Accepted")).scalar():
        db.session.add(state_accepted)
    if not db.session.query(exists().where(State.name == "Declined")).scalar():
        db.session.add(state_declined)

    db.session.commit()

    USER_DATASTORE.find_or_create_role(name='Admin')
    USER_DATASTORE.find_or_create_role(name='Employee')
    USER_DATASTORE.find_or_create_role(name='View')

    if not USER_DATASTORE.get_user('admin@admin.com'):
        USER_DATASTORE.create_user(email='admin@admin.com',
                                   password=utils.encrypt_password('admin'))

    db.session.commit()

    USER_DATASTORE.add_role_to_user('admin@admin.com', 'Admin')
    db.session.commit()


@login_required
@roles_accepted('Admin', 'Employee')
@app.route('/set_date_vacation_ajax', methods=['POST'])
def set_date_vacation_ajax():
    """set vacation days ajax"""
    date = request.json['date']
    date = datetime.strptime(str(date), '%Y-%m-%d')
    operation = request.json['operation']
    if str(operation) == "insert":
        date = db.session.query(AvaliableVacationDay.id).filter_by(avaliable_day=date).scalar()
        state = db.session.query(State.id).filter_by(name="Pending").scalar()
        user_vacation = UserAvaliableVacationDays(vacation_day_id=date,
                                                  user_id=current_user.id,
                                                  state_id=state)
        db.session.add(user_vacation)
        db.session.commit()
    if str(operation) == "delete":
        date = db.session.query(AvaliableVacationDay).filter_by(avaliable_day=date).first()
        this_date = db.session.query(UserAvaliableVacationDays).filter_by(vacation_day_id=date.id, user_id=current_user.id).first()
        db.session.delete(this_date)
        db.session.commit()
    return "Sucsess"


@login_required
@roles_accepted('Admin', 'Employee')
@app.route('/get_date_vacation_ajax', methods=['POST'])
def get_date_vacation_ajax():
    """get vacation days ajax"""
    vacation_dates = db.session.query(UserAvaliableVacationDays).filter_by(user_id=current_user.id).all()
    data = []
    for dates in vacation_dates:
        row = {}
        vacation_id = dates.vacation_day_id
        date = db.session.query(AvaliableVacationDay.avaliable_day).filter_by(id=vacation_id).scalar()
        new_date = str(date).split(' ')
        row["avaliable_day"] = new_date[0]
        row["status"] = str(dates.states.name)
        data.append(row)

    return json.dumps(data)


@login_required
@roles_accepted('Admin')
@app.route('/set_date_ajax', methods=['POST'])
def set_date_ajax():
    """set date ajax"""
    date = request.json['date']
    date = datetime.strptime(str(date), '%Y-%m-%d')
    operation = request.json['operation']
    if str(operation) == "insert":
        newdate = AvaliableVacationDay(avaliable_day=date)
        db.session.add(newdate)
        db.session.commit()
    if str(operation) == "delete":
        this = AvaliableVacationDay.query.filter_by(avaliable_day=date).first()
        db.session.delete(this)
        db.session.commit()
    return "Sucsess"


@login_required
@roles_accepted('Admin', 'Employee', 'View')
@app.route('/get_date_ajax', methods=['POST'])
def get_date_ajax():
    """get date ajax"""
    dates = AvaliableVacationDay.query.all()
    avaliable_vacation_day_schema = AvaliableVacationDaySchema(many=True)
    result = avaliable_vacation_day_schema.dumps(dates)
    return result.data


@app.route('/')
@app.route('/index')
@login_required
@roles_accepted('Admin', 'Employee', 'View')
def index():
    """home page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flask.flash('Logged in successfully.')
        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)
        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """register"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=utils.encrypt_password(form.password.data), active=False)
        db.session.add(user)
        db.session.commit()
        USER_DATASTORE.add_role_to_user(form.email.data, 'View')
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    """logout"""
    logout_user()
    return redirect(url_for('index'))
