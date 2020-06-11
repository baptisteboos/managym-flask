from flask import render_template, url_for, redirect, flash, g, \
    request, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.main import bp
from app.models import Athlete, Event, Permission
from app.main.forms import EventRegisterForm
from app.decorators import admin_required, permission_required


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    athletes = current_user.athletes_in_groups().all()
    print(athletes[0].birth_date)
    return render_template('index.html', user=current_user, title=_('index'), athletes=athletes)

@bp.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html', title=_('Administration'))

@bp.route('/events')
@login_required
@permission_required(Permission.READ)
def events():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date.desc()).paginate(page, current_app.config['ATHLETES_PER_PAGE'], False)
    next_url = url_for('main.events', page=events.next_num) \
        if events.has_next else None
    prev_url = url_for('main.events', page=events.prev_num) \
        if events.has_prev else None
    return render_template('events.html', title=_('Events index'), events=events.items, \
        next_url=next_url, prev_url=prev_url)

@bp.route('/event/register', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CREATE)
def event_register():
    form = EventRegisterForm()
    if form.validate_on_submit():
        event = Event(name=form.name.data, description=form.description.data,
                      date=form.date.data, place=form.place.data)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('main.events'))
    return render_template('event_register.html', form=form, title=_('Register event'))

