from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Required, Email
from wtforms.fields.html5 import DateField

class RegistrationAthleteForm(FlaskForm):
    first_name = StringField(_l('First_name'), validators=[DataRequired()])
    last_name = StringField(_l('Last_name'), validators=[DataRequired()])
    gender = RadioField(_l('Gender'), choices=[('1', _l('male')), ('2', _l('female'))], coerce=str)
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    date_birth = DateField(_l('Date of birth'), format='%Y-%m-%d', validators=[Required()])
    submit = SubmitField(_l('Register'))