from flask import render_template, url_for, redirect, flash, g, request
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.main import bp
from app.models import Athlete, Group
from app.main.forms import AthleteRegisterForm, AthleteEditForm, EmptyForm


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    athletes = Athlete.query.all()
    return render_template('index.html', user=current_user, title=_('index'), athletes=athletes)

@bp.route('/athlete/register', methods=['GET', 'POST'])
@login_required
def athlete_register():
    form = AthleteRegisterForm()
    form.set_choices()
    if form.validate_on_submit():
        athlete = Athlete(first_name=form.first_name.data.capitalize(), \
                          last_name=form.last_name.data.capitalize(), \
                          email=form.email.data, gender=form.gender.data, birth_date=form.birth_date.data)
        db.session.add(athlete)
        db.session.commit()
        flash(_('Succesfully athlete added'))
        return redirect(url_for('main.index'))
    return render_template('athlete_register.html', form=form, title=_('Registration'))


@bp.route('/athlete/<int:id>')
@login_required
def athlete(id):
    athlete = Athlete.query.get_or_404(id)
    form = EmptyForm()
    return render_template('athlete.html', athlete=athlete, form=form)

@bp.route('/athlete/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def athlete_edit(id):
    athlete = Athlete.query.get_or_404(id)
    form = AthleteEditForm()
    if form.validate_on_submit():
        athlete.email = form.email.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.athlete', id=id))
    elif request.method == 'GET':
        form.email.data = athlete.email
    return render_template('athlete_edit.html', title=_('Edit athlete'), form=form)

@bp.route('/athlete/<int:id>/new_target', methods=['POST'])
@login_required
def athlete_new_target(id):
    EVENT_ID = 1
    form = EmptyForm()
    if form.validate_on_submit():
        athlete = Athlete.query.get_or_404(id)
        athlete.new_target_results(event_id=EVENT_ID)
        db.session.commit()
        flash(_('New target create.'))
        return redirect(url_for('main.athlete', id=id))     
    else:
        return redirect(url_for('main.index'))

@bp.route('/athlete/<int:id>/delete_target', methods=['POST'])
@login_required
def athlete_delete_target(id):
    EVENT_ID = 1
    form = EmptyForm()
    if form.validate_on_submit():
        athlete = Athlete.query.get_or_404(id)
        if athlete.target_results.all():
            athlete.delete_target_results(event_id=EVENT_ID)
            db.session.commit()
            flash(_('Target deleted.'))
            return redirect(url_for('main.athlete', id=id))
    return redirect(url_for('main.index'))
