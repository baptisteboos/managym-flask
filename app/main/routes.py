from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_babel import _

from app import db
from app.main import bp
from app.models import Athlete
from app.main.forms import RegistrationAthleteForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    athletes = Athlete.query.all()
    return render_template('index.html', user=current_user, title=_('index'), athletes=athletes)

@bp.route('/players/register', methods=['GET', 'POST'])
@login_required
def register_player():
    form = RegistrationAthleteForm()
    if form.validate_on_submit():
        athlete = Athlete(first_name=form.first_name.data.capitalize(), \
                          last_name=form.last_name.data.capitalize(), \
                          gender=form.gender.data, date_birth=form.date_birth.data)
        db.session.add(athlete)
        db.session.commit()
        flash(_('Succesfully athlete added'))
        return redirect(url_for('main.index'))
    return render_template('register_athlete.html', form=form, title=_('Registration'))