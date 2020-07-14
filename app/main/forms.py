from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from wtforms.fields.html5 import DateField

from app.models import TypeEvent


class EventForm(FlaskForm):
    """docstring for EventRegisterForn"""
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[Length(max=140)])
    date = DateField(_l('Date'), validators=[DataRequired()])
    place = StringField(_l('Place'), validators=[DataRequired()])
    type_id = SelectField(_l('Type'), coerce=int)
    submit = SubmitField(_l('Register'))

    def set_choices(self):
        self.type_id.choices = [(g.id, g.name) for g in TypeEvent.query.order_by('name')]