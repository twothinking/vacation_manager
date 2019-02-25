from app import db, ma, login
import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class UserAvaliableVacationDays(db.Model):
	__tablename__ = 'user_avaliable_vacation_day'
	id = Column(Integer, primary_key=True,autoincrement=True)
	vacation_day_id = Column(Integer, ForeignKey('avaliable_vacation_day.id',ondelete="CASCADE"))
	user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"))
	state_id = Column(Integer, ForeignKey('state.id',ondelete="CASCADE"))

	avaliable_vacation_day = relationship("AvaliableVacationDay",
							backref=backref("user_avaliable_vacation_day",cascade='all,delete-orphan',lazy='dynamic'))

	users = relationship("User",
							backref=backref("user_avaliable_vacation_day",cascade='all,delete-orphan',lazy='dynamic'))

	states = relationship("State",
							backref=backref("user_avaliable_vacation_day",cascade='all,delete-orphan',lazy='dynamic'))
	

class UserAvaliableVacationDaysSchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('vacation_day_id','user_id','state_id')

class AvaliableVacationDay(db.Model):
	__tablename__ = 'avaliable_vacation_day'
	id = db.Column(db.Integer, primary_key=True)
	avaliable_day = db.Column(db.DateTime())
	
	def __str__(self):
		return str(self.avaliable_day).split(" ")[0]


class AvaliableVacationDaySchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('avaliable_day',)

class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(128), nullable=False, server_default='')
	active = db.Column(db.Boolean())
	email_confirmed_at = db.Column(db.DateTime())
	roles = db.relationship("Role",secondary='user_roles')

	def __str__(self):
		return self.email


class State(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)

	def __repr__(self):
		return '<State %r>' % (self.name)

	def __str__(self):
		return self.name


class Role(RoleMixin,db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)

	def __str__(self):
		return self.name

class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))