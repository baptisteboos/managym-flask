from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Required
from wtforms.fields.html5 import DateField


class RegistrationPlayerForm(FlaskForm):
	first_name = StringField('First_name', validators=[DataRequired()])
	last_name = StringField('Last_name', validators=[DataRequired()])
	gender = RadioField('Gender', choices=[('1', 'male'), ('2', 'female')], coerce=str)
	date_birth = DateField('Date of birth', format='%Y-%m-%d', validators=[Required()])
	submit = SubmitField('Register')