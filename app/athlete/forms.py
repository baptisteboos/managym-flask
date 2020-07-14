from flask import request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, RadioField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField

from app.models import Group

class AthleteForm(FlaskForm):
    first_name = StringField(_l('First name'), validators=[DataRequired()])
    last_name = StringField(_l('Last name'), validators=[DataRequired()])
    birth_date = DateField(_l('Date of birth'), format='%Y-%m-%d', validators=[DataRequired()])
    gender = RadioField(_l('Gender'), choices=[('1', _l('Male')), ('2', _l('Female'))], coerce=str)
    email = StringField(_l('Email'))
    email_2 = StringField(_l('Email 2'))
    phone_number = StringField(_l('Phone number'))
    phone_number_2 = StringField(_l('Phone number 2'))
    address = StringField(_l('Address'))
    city = StringField(_l('City'))
    province = SelectField(_l('province'), choices=[('QC', 'QC')])
    postal_code = StringField(_l('Postal code'))
    group_id = SelectField(_l('Group'), coerce=int)
    submit = SubmitField(_l('Register'))

    def set_choices(self):
        self.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]

class EmptyForm(FlaskForm):
    submit = SubmitField(_('Submit'))

class NewTargetResultsForm(FlaskForm):
    event = SelectField(_l('Event', coerce=int))
    submit = SubmitField(_l('Submit'))

    def set_choices(self, list_tuples):
        self.event.choices = [(e.id, e.name) for e in list_tuples]

class SearchForm(FlaskForm):
    q = StringField(_l('Search for athletes...'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class InformationForm(FlaskForm):
    information = TextAreaField(_l('Write something'), validators=[DataRequired()]) 
    submit = SubmitField(_l('Submit'))
