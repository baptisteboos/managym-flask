import os
import base64
import jwt
from time import time

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    date_birth = db.Column(db.DateTime, 
                           index=False,
                           unique=False,
                           nullable=False)
    group_id = db.Column(db.Integer,
                         db.ForeignKey('group.id'))

    def __repr__(self):
        return f'<Athlete {self.first_name} {self.last_name}>'

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


