from datetime import date
import jwt
import pytest
from app import create_app, db
from app.models import User, Athlete, Apparel, Event, TargetResults
from config import Config

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestUserModel:
	def setup_method(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def teardown_method(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_password_hashing(self):
		u = User(username='Bobby')
		u.set_password('kid')
		assert not u.check_password('cat')
		assert u.check_password('kid')

	def test_reset_password_token(self):
		u = User(username='Patpat', first_name='Patrick', last_name='python', email='pat@test.com')
		u.set_password('patpat')
		db.session.add(u)
		db.session.commit()
		token = u.get_reset_password_token()
		assert u == User.verify_reset_password_token(token)

class TestTargetResultsModel:
	def setup_method(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

		# We create few data for all tests
		at1 = Athlete(first_name='Terminator', last_name='T-800', \
					  gender='1', birth_date=date(1984, 10, 26))
		at2 = Athlete(first_name='John', last_name='Rambo', \
					  gender='1', birth_date=date(1947, 7, 6))
		db.session.add_all([at1, at2])
		db.session.commit()

		ap1 = Apparel(short_name='FX', name='floor exercice')
		ap2 = Apparel(short_name='PH', name='pommel horse')
		ap3 = Apparel(short_name='SR', name='still rings')
		ap4 = Apparel(short_name='VT', name='vault')
		ap5 = Apparel(short_name='PB', name='parallel bars')
		ap6 = Apparel(short_name='HB', name='high bar')
		db.session.add_all([ap1, ap2, ap3, ap4, ap5, ap6])
		db.session.commit()

		ev = Event(name='2nd World cup', date=date(2020, 3, 5), place='Mt Olympe')
		db.session.add(ev)
		db.session.commit()

		tg1 = TargetResults(athlete_id=1, apparel_id=1, event_id=1, \
							target_sv=5.0, target_ex=8.5, \
							result_sv=4.5, result_ex=9.0)
		tg2 = TargetResults(athlete_id=1, apparel_id=5, event_id=1, \
							target_sv=4.5, target_ex=9.5, \
							result_sv=4.5, result_ex=9.3)
		tg3 = TargetResults(athlete_id=2, apparel_id=1, event_id=1, \
							target_sv=6.5, target_ex=9.0, \
							result_sv=6.5, result_ex=7.0)
		db.session.add_all([tg1, tg2, tg3])
		db.session.commit()

	def teardown_method(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()


	def test_constructor(self):
		a = Athlete.query.filter_by(first_name='Terminator').first()
		assert a.target_results.count() == 2
		assert a.target_results.count() == TargetResults.query.filter_by(athlete_id=1).count()
		assert a.target_results.first().result_sv == 4.5
		assert a.target_results.first().target_total == 13.5
		assert a.target_results.first().result_total == 13.5
		assert a.target_results.first().target_result_total == 100,00

		ev = Event.query.get(1)
		assert ev.target_results.count() == 3

		tg = TargetResults.query.get(1)
		assert tg.athlete == a
		assert tg.event == ev

		score = a.target_results_from_event(1)
		print(score)

		

