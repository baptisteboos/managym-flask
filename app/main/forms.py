from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from wtforms.fields.html5 import DateField

class EventRegisterForm(FlaskForm):
	"""docstring for EventRegisterForn"""
	name = StringField(_l('Name'), validators=[DataRequired()])
	description = StringField(_l('Description'), validators=[Length(max=140)])
	date = DateField(_l('Date'), validators=[DataRequired()])
	place = StringField(_l('Place'), validators=[DataRequired()])
	submit = SubmitField(_l('Register'))
