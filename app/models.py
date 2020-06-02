import os
import base64

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

@login.user_loader
def load_user(id):
  return User.query.get(int(id))


class Player(db.Model):
    id = db.Column(db.Integer, 
                   primary_key=True)
    first_name = db.Column(db.String(64),
                           index=False,
                           unique=False,
                           nullable=False)
    last_nane = db.Column(db.String(64),
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

    def __repr__(self):
        return f'<Player {self.first_name} {self.last_name}>'


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
                     nullable=False)
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


