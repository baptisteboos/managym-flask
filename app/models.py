import os
import base64
from hashlib import md5
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


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

@login.user_loader
def load_user(id):
  return User.query.get(int(id))


class TargetResults(db.Model):
    __tablename__ = 'target_results'
    id = db.Column(db.Integer, 
                   primary_key=True)
    athlete_id = db.Column(db.Integer, 
                           db.ForeignKey('athlete.id'),
                           nullable=False)
    apparel_id = db.Column(db.Integer, 
                           db.ForeignKey('apparel.id'),
                           nullable=False)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('event.id'),
                         nullable=False)
    
    __table_args__ = (db.UniqueConstraint(athlete_id, apparel_id, event_id),)

    target_sv = db.Column(db.Float,
                          nullable=True)
    target_ex = db.Column(db.Float,
                          nullable=True)
    result_sv = db.Column(db.Float,
                          nullable=True)
    result_ex = db.Column(db.Float,
                          nullable=True)
    # Simple relation don't need a backref for the moment
    apparel = db.relationship('Apparel')

    def __repr__(self):
        return f'<TargetResults: {self.athlete_id}, {self.apparel_id}, {self.event_id}'

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
                score[result.apparel.short_name.upper()] = result
        # elif not target_results and self.gender ==  '2':
        #     target_results = {'VT': [], 'UB': [], 'BB': [], 'FX': []}
        else: 
            return  
        return score

    def new_target_results(self, event_id):
        list_target_results = [TargetResults(athlete_id=self.id, event_id=event_id,
            apparel_id=i, target_sv=0, target_ex=0, result_sv=0, result_ex=0)
            for i in range(1, 7)]
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


class Apparel(db.Model):
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

class TargetScore():
    def __init__(self, target_sv, target_ex, result_sv, result_ex):
        self.target_sv = target_sv
        self.target_ex = target_ex
        self.result_sv = result_sv
        self.result_ex = result_ex

    @staticmethod
    def target_total(self):
        return self.target_sv + self.target_ex
