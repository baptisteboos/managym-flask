import os
import base64
from hashlib import md5
from time import time
from datetime import datetime

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)
    username = db.Column(db.String(64), 
                         index=True, 
                         unique=True,
                         nullable=False)    
    first_name = db.Column(db.String(64),
                           index=False,
                           unique=False,
                           nullable=False)
    last_name = db.Column(db.String(64),
                          index=False,
                          unique=False,
                          nullable=False)
    email = db.Column(db.String(120), 
                      index=True,
                      unique=True, 
                      nullable=False)
    salt = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,
                        db.ForeignKey('roles.id'))
    groups = db.relationship('Group', secondary=user_group, 
        lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
    informations = db.relationship('Information', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        # generate a random salt
        self.salt = str(base64.b64encode(os.urandom(16)))
        self.password_hash = generate_password_hash(self.salt + password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, self.salt + password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], \
        algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def can(self, permissions):
        return self is not None and \
            (self.role.permissions & permissions) == permissions # bitwise operation

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def athletes_in_groups(self):
        return Athlete.query.join(Group, (Athlete.group_id == Group.id)).join(
            user_group, (user_group.c.group_id == Group.id)).filter(
            user_group.c.user_id == self.id).order_by(Athlete.last_name)


@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Permission:
    READ = 0x01
    EDIT = 0x02
    CREATE = 0x04
    DELETE = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # Should be set True only for one role and False for the others
    default = db.Column(db.Boolean, default=False, index=True)
    # Is used as bit flags, each tacks will be assigned a bit position
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.READ, True),
            'Moderator': (Permission.READ |
                          Permission.EDIT |
                          Permission.CREATE |
                          Permission.DELETE, False),
            'Adminisrator': (0xff, False)
        }
        for r in roles:
            # Tried to find an existant role to update it otherwise we create a new one
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()



class TargetResults(db.Model):
    __tablename__ = 'target_results'
    id = db.Column(db.Integer, 
                   primary_key=True)
    athlete_id = db.Column(db.Integer, 
                           db.ForeignKey('athlete.id'),
                           nullable=False)
    apparatus_id = db.Column(db.Integer, 
                           db.ForeignKey('apparatus.id'),
                           nullable=False)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('event.id'),
                         nullable=False)
    
    __table_args__ = (db.UniqueConstraint(athlete_id, apparatus_id, event_id),)

    target_sv = db.Column(db.Float,
                          nullable=True)
    target_ex = db.Column(db.Float,
                          nullable=True)
    result_sv = db.Column(db.Float,
                          nullable=True)
    result_ex = db.Column(db.Float,
                          nullable=True)
    # Simple relation don't need a backref for the moment
    apparatus = db.relationship('Apparatus')

    def __repr__(self):
        return f'<TargetResults: {self.athlete_id}, {self.apparatus_id}, {self.event_id}'

    @property
    def target_total(self):
        return round(self.target_sv + self.target_ex, 2)

    @property
    def result_total(self):
        return round(self.result_sv + self.result_ex, 2)

    @property
    def target_result_sv(self):
        if self.target_sv != 0:
            return round(self.result_sv / self.target_sv * 100, 2)
        return 0

    @property
    def target_result_ex(self):
        if self.target_ex != 0:
            return round(self.result_ex / self.target_ex * 100, 2)
        return 0

    @property
    def target_result_total(self):
        if (self.target_sv + self.target_ex) != 0:
            return round((self.result_sv + self.result_ex) / (self.target_sv + self.target_ex) * 100, 2)
        return 0

class Group(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(120),
                     index=True,
                     unique=True,
                     nullable=False)
    athletes = db.relationship('Athlete', backref='group', lazy='dynamic')

    def __repr__(self):
        return f'<Group: {self.name}>'


class Athlete(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)
    first_name = db.Column(db.String(64),
                           index=False,
                           unique=False,
                           nullable=False)
    last_name = db.Column(db.String(64),
                          index=False,
                          unique=False,
                          nullable=False)
    email = db.Column(db.String(120), 
                      index=False,
                      unique=False, 
                      nullable=True)
    gender = db.Column(db.String(1), # 0=Not known, 1=male, 2=female, 9=Not applicable (ISO 5218)
                       nullable=False)
    birth_date = db.Column(db.DateTime, 
                           index=False,
                           unique=False,
                           nullable=False)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('group.id'),
                         nullable=True)
    # target_results return a query with lazy='dynamic', can apply additional SQL filters
    # /!\ the reverse 'TargetResults.athlete' return an object Athlete
    target_results = db.relationship('TargetResults', backref='athlete', lazy='dynamic')
    informations = db.relationship('Information', backref='athlete', lazy='dynamic')

    def __repr__(self):
        return f'<Athlete {self.first_name} {self.last_name}>'

    def picture(self, size):
        email = self.email or 'email@test.com'
        digest = md5(email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def target_results_from_event(self, event_id):
        id = Event.query.get(event_id)
        if not id:
            return
        target_results = self.target_results.filter_by(event_id=event_id).all()
        if target_results and self.gender == '1':
            score = {'FX': None, 'PH': None, 'SR': None, 'VT': None, 'PB': None, 'HB': None}
            for result in target_results:
                score[result.apparatus.short_name.upper()] = result
        elif target_results and self.gender == '2':
            score = {'VT': None, 'UB': None, 'BB': None, 'FX': None}
            for result in target_results:
                score[result.apparatus.short_name.upper()] = result
        else: 
            return  
        return score

    def new_target_results(self, event_id):
        if self.gender == '1':
            list_target_results = [TargetResults(athlete_id=self.id, event_id=event_id,
                apparatus_id=i, target_sv=0, target_ex=0, result_sv=0, result_ex=0)
                for i in range(1, 7)]
        elif self.gender == '2':
            list_target_results = [TargetResults(athlete_id=self.id, event_id=event_id,
                apparatus_id=i, target_sv=0, target_ex=0, result_sv=0, result_ex=0)
                for i in [1,4,7,8]] # Floor, vault, Balance beam, Uneven bars
        db.session.add_all(list_target_results)

    def delete_target_results(self, event_id):
        TargetResults.query.filter_by(athlete_id=self.id, event_id=event_id).delete()

class Event(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.String(128), 
                     index=True,
                     unique=False,
                     nullable=False)
    description = db.Column(db.String(140),
                            index=False,
                            unique=False,
                            nullable=True)
    date = db.Column(db.DateTime, 
                     index=False,
                     unique=False,
                     nullable=False) # date = form.date_birth.data.split('-')
        # athlete = Athlete(first_name=form.first_name.data.capitalize(), \
        #                   last_name=form.last_name.data.capitalize(), \
        #                   gender=form.gender.data, date_birth=form.date_birth.data)
    place = db.Column(db.String(120),
                      index=False,
                      unique=False,
                      nullable=False)
    # target_results return a query with lazy='dynamic', can apply additional SQL filters
    # /!\ the reverse 'TargetResults.event' return an object Event
    target_results = db.relationship('TargetResults', backref='event', lazy='dynamic')

    def __repr__(self):
        return f'<Event {self.name}>'


class Apparatus(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)
    short_name = db.Column(db.String(3), 
                           index=True,
                           unique=True,
                           nullable=False) 
    name = db.Column(db.String(30), 
                     index=True,
                     unique=True,
                     nullable=False) 

    def __repr__(self):
        return f'<Name {self.name}>'

class Information(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    body = db.Column(db.Text,
                 unique=False,
                 nullable=True)
    timestamp = db.Column(db.DateTime,
                          index=True, 
                          default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type_information.id'))

    def __repr__(self):
        return f'<Info {self.body}>'

class TypeInformation(db.Model):
    """docstring for TypeInformation"""
    __tablename__ = 'type_information'

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(64),
                     index=False,
                     unique=True,
                     nullable=False)
    messages = db.relationship('Information', backref='type', lazy='dynamic')

    def __repr__(self):
        return f'<Type {self.name}>'
        

