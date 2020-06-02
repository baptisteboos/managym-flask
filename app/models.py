import os
import base64

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(120), unique=True, index=True)
	salt = db.Column(db.String())
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return f'<User {self.username}>'

	def set_password(self, password):
		# generate a random salt
		self.salt = str(base64.b64encode(os.urandom(16)))
		self.password_hash = generate_password_hash(self.salt + password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, self.salt + password)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(120))
	gender = db.Column(db.String(1), nullable=False)
	date_birth = db.Column(db.DateTime, nullable=False)

	def __repr__(self):
		return f'<Player {self.first_name} {self.last_name}>'

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False, index=True)
	description = db.Column(db.String(140))
	date = db.Column(db.DateTime, nullable=False)

	def __repr__(self):
		return f'<Event {self.name}>'

class Apparel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	short_name = db.Column(db.String(3), unique=True, index=True)
	name = db.Column(db.String(30), unique=True, index=True)

	def __repr__(self):
		return f'<Name {self.name}>'


