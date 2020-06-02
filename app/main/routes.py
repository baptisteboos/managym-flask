from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import RegistrationPlayerForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = {'first_name': 'Patrick'}
    return render_template('index.html', user=user, title='index')

@bp.route('/players/register', methods=['GET', 'POST'])
@login_required
def register_player():
    form = RegistrationPlayerForm()
    if form.validate_on_submit():
        flash(f'gender= {form.gender.data}, date= {form.date_birth.data}')
        return redirect(url_for('index'))
    return render_template('register_player.html', form=form, title='Registration')