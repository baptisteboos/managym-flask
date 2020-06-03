from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_babel import _

from app import db
from app.main import bp
from app.models import Athlete, Group
from app.main.forms import RegistrationAthleteForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    athletes = Athlete.query.all()
    return render_template('index.html', user=current_user, title=_('index'), athletes=athletes)

@bp.route('/athlete/register', methods=['GET', 'POST'])
@login_required
def register_athlete():
    form = RegistrationAthleteForm()
    form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
    if form.validate_on_submit():
        athlete = Athlete(first_name=form.first_name.data.capitalize(), \
                          last_name=form.last_name.data.capitalize(), \
                          email=form.email.data, gender=form.gender.data, date_birth=form.date_birth.data)
        db.session.add(athlete)
        db.session.commit()
        flash(_('Succesfully athlete added'))
        return redirect(url_for('main.index'))
    return render_template('register_athlete.html', form=form, title=_('Registration'))


@bp.route('/athlete/<int:id>')
@login_required
def athlete(id):
    athlete = Athlete.query.get_or_404(id)
    return render_template('athlete.html', athlete=athlete)