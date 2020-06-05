from flask import render_template, url_for, redirect, flash, g, request
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.main import bp
from app.models import Athlete


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    athletes = Athlete.query.all()
    return render_template('index.html', user=current_user, title=_('index'), athletes=athletes)


