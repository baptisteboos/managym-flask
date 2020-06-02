from flask import render_template, url_for, redirect, flash
from app import app
from app.forms import RegistrationPlayerForm

@app.route('/')
@app.route('/index')
def index():
	user = {'first_name': 'Patrick'}
	return render_template('index.html', user=user, title='index')

@app.route('/players/register', methods=['GET', 'POST'])
def register_player():
	form = RegistrationPlayerForm()
	if form.validate_on_submit():
		flash(f'gender= {form.gender.data}, date= {form.date_birth.data}')
		print('lol')
		return redirect(url_for('index'))
	return render_template('register_player.html', form=form, title='Registration')