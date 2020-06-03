from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, RadioField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import DateField

from app.models import Group

class RegistrationAthleteForm(FlaskForm):
    first_name = StringField(_l('First_name'), validators=[DataRequired()])
    last_name = StringField(_l('Last_name'), validators=[DataRequired()])
    gender = RadioField(_l('Gender'), choices=[('1', _l('male')), ('2', _l('female'))], coerce=str)
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    birth_date = DateField(_l('Date of birth'), format='%Y-%m-%d', validators=[DataRequired()])
    group_id = SelectField(_l('Group'), coerce=int)
    submit = SubmitField(_l('Register'))

    def set_choices(self):
    	self.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]