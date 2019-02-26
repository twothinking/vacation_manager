"""Models"""

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from vacation_manager import ma, db, login


# pylint: disable=no-member, too-few-public-methods


class UserAvaliableVacationDays(db.Model):
    """Avaliable vacation days"""
    __tablename__ = 'user_avaliable_vacation_day'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vacation_day_id = Column(Integer, ForeignKey('avaliable_vacation_day.id', ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    state_id = Column(Integer, ForeignKey('state.id', ondelete="CASCADE"))

    avaliable_vacation_day = relationship("AvaliableVacationDay",
                                          backref=backref("user_avaliable_vacation_day",
                                                          cascade='all,delete-orphan',
                                                          lazy='dynamic'))

    users = relationship("User",
                         backref=backref("user_avaliable_vacation_day",
                                         cascade='all,delete-orphan',
                                         lazy='dynamic'))

    states = relationship("State",
                          backref=backref("user_avaliable_vacation_day",
                                          cascade='all,delete-orphan',
                                          lazy='dynamic'))


class UserAvaliableVacationDaysSchema(ma.Schema):
    """user avaliable vacation dys"""
    class Meta:
        """Meta informations"""
        # Fields to expose
        fields = ('vacation_day_id', 'user_id', 'state_id')


class AvaliableVacationDay(db.Model):
    """Avaliable vacation days"""
    __tablename__ = 'avaliable_vacation_day'
    id = db.Column(db.Integer, primary_key=True)
    avaliable_day = db.Column(db.DateTime())

    def __str__(self):
        return str(self.avaliable_day).split(" ")[0]


class AvaliableVacationDaySchema(ma.Schema):
    """Avaliable vacation days"""
    class Meta:
        """Meta data"""
        # Fields to expose
        fields = ('avaliable_day',)


class User(UserMixin, db.Model):
    """Users"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    email_confirmed_at = db.Column(db.DateTime())
    roles = db.relationship("Role", secondary='user_roles')

    def __str__(self):
        return self.email


class State(db.Model):
    """State"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<State %r>' % (self.name)

    def __str__(self):
        return self.name


class Role(RoleMixin, db.Model):
    """Role"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name


class UserRoles(db.Model):
    """User roles"""
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


@login.user_loader
def load_user(uid):
    """Load Users"""
    return User.query.get(int(uid))
