from flask import render_template, url_for, redirect, flash, g, request, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale

from app import db
from app.athlete import bp
from app.models import Athlete, Group, TargetResults, Permission, Event, \
    Information, AthleteEvent
from app.athlete.forms import AthleteRegisterForm, AthleteEditForm, EmptyForm,\
    SearchForm, NewTargetResultsForm, InformationForm
from app.decorators import permission_required

@bp.route('/register', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CREATE)
def athlete_register():
    form = AthleteRegisterForm()
    form.set_choices()
    if form.validate_on_submit():
        athlete = Athlete(first_name=form.first_name.data.capitalize(), \
                          last_name=form.last_name.data.capitalize(), \
                          gender=form.gender.data, \
                          birth_date=form.birth_date.data)
        athlete.email = form.email.data
        athlete.email_2 = form.email_2.data
        athlete.phone_number = form.phone_number.data
        athlete.phone_number_2 = form.phone_number_2.data
        athlete.address = form.address.data
        athlete.city = form.city.data
        athlete.postal_code = form.postal_code.data
        athlete.group_id = form.group_id.data
        db.session.add(athlete)
        db.session.commit()
        flash(_('Succesfully athlete added'))
        return redirect(url_for('athlete.athletes'))
    return render_template('athlete/athlete_register.html', form=form, title=_('Registration'))

@bp.route('/')
@login_required
@permission_required(Permission.READ)
def athletes():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    athletes = Athlete.query.order_by('last_name').paginate(page, current_app.config['ATHLETES_PER_PAGE'], False)
    next_url = url_for('athlete.athletes', page=athletes.next_num) \
        if athletes.has_next else None
    prev_url = url_for('athlete.athletes', page=athletes.prev_num) \
        if athletes.has_prev else None
    return render_template('athlete/athletes.html', title=_('Athlete index'), athletes=athletes.items, \
        next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.READ)
def athlete(id):
    athlete = Athlete.query.get_or_404(id)
    events_participated = Event.query.join(TargetResults).filter(\
                          TargetResults.athlete_id == id).order_by(\
                          Event.date.desc()).all()

    # Event object required
    query = db.session.query(Event.id, Event.name)
    # All the event_id that an athlete participates
    subquery = db.session.query(TargetResults.event_id).filter(\
        TargetResults.athlete_id == id).distinct()
    # Event that an athlete has not target/resuts
    events = query.filter(~Event.id.in_(subquery)).all()

    target_form = NewTargetResultsForm()
    target_form.set_choices(events)
    information_form = InformationForm()
    if information_form.validate_on_submit():
        TYPE_ID = 1
        info = Information(body=information_form.information.data, user_id=current_user.id, type_id=TYPE_ID)
        athlete.informations.append(info)
        db.session.commit()
        return redirect(url_for('athlete.athlete', id=id))
    return render_template('athlete/athlete.html', athlete=athlete, target_form=target_form, \
        information_form=information_form, events_participated=events_participated)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT)
def athlete_edit(id):
    athlete = Athlete.query.get_or_404(id)
    form = AthleteEditForm()
    form.set_choices()
    if form.validate_on_submit():
        print('save')
        athlete.first_name = form.first_name.data.capitalize()
        athlete.last_name = form.last_name.data.capitalize()
        athlete.birth_date = form.birth_date.data
        athlete.gender = form.gender.data
        athlete.email = form.email.data
        athlete.email_2 = form.email_2.data
        athlete.phone_number = form.phone_number.data
        athlete.phone_number_2 = form.phone_number_2.data
        athlete.address = form.address.data
        athlete.city = form.city.data
        athlete.postal_code = form.postal_code.data
        athlete.group_id = form.group_id.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('athlete.athlete', id=id))
    elif request.method == 'GET':
        form.first_name.data = athlete.first_name
        form.last_name.data = athlete.last_name
        form.birth_date.data = athlete.birth_date
        form.gender.data = athlete.gender
        form.email.data = athlete.email
        form.email_2.data = athlete.email_2
        form.phone_number.data = athlete.phone_number
        form.phone_number_2.data = athlete.phone_number_2
        form.address.data = athlete.address
        form.city.data = athlete.city
        form.postal_code.data = athlete.postal_code
        form.group_id.data = athlete.group_id
    return render_template('athlete/athlete_edit.html', title=_('Edit athlete'), form=form)

@bp.route('/<int:id>/new_target', methods=['POST'])
@login_required
@permission_required(Permission.CREATE)
def athlete_new_target(id):
    event_id = request.form['event']
    form = EmptyForm()
    if form.validate_on_submit():
        athlete = Athlete.query.get_or_404(id)
        athlete.new_target_results(event_id=event_id)
        athlete_event = AthleteEvent(athlete_id=id, event_id=event_id,
                                     target_total=0, result_total=0)
        db.session.add(athlete_event)
        db.session.commit()
        flash(_('New target create.'))
        return redirect(url_for('athlete.athlete', id=id))     
    else:
        return redirect(url_for('athlete.athletes'))

@bp.route('/<int:id>/delete_target', methods=['POST'])
@login_required
@permission_required(Permission.DELETE)
def athlete_delete_target(id):
    event_id = request.args.get('event', 0, int)
    Event.query.get_or_404(event_id)
    form = EmptyForm()
    if form.validate_on_submit():
        athlete = Athlete.query.get_or_404(id)
        if athlete.target_results.all():
            athlete.delete_target_results(event_id=event_id)
            athlete.events.filter_by(event_id=event_id).delete()
            db.session.commit()
            flash(_('Target deleted.'))
            return redirect(url_for('athlete.athlete', id=id))
    return redirect(url_for('athlete.athletes'))

@bp.route('/<int:id>/update_target', methods=['POST'])
@login_required
@permission_required(Permission.EDIT)
def athlete_update_target(id):
    event_id = request.form['event_id']
    apparatus_id = request.form['apparatus_id']
    target_result = TargetResults.query.filter_by(athlete_id=id, event_id=event_id, \
                                                  apparatus_id=apparatus_id).first()
    target_result.target_sv = request.form['tsv']
    target_result.target_ex = request.form['tex']
    target_result.result_sv = request.form['rsv']
    target_result.result_ex = request.form['rex']

    athlete_event = AthleteEvent.query.filter_by(athlete_id=id, \
                                                 event_id=event_id).first()
    athlete_event.target_total = request.form['target']
    athlete_event.result_total = request.form['result']

    db.session.commit()
    return redirect(url_for('athlete.athlete', id=id))

@bp.route('/search')
@login_required
@permission_required(Permission.READ)
def search():
    # if not search_form.validate():
    #     return redirect(url_for('main.explore'))
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    search = f"%{request.args.get('q', ' ').capitalize()}%"
    athletes = Athlete.query.filter((Athlete.first_name.like(search)) | \
        (Athlete.last_name.like(search))).order_by(Athlete.last_name).\
        paginate(page, current_app.config['ATHLETES_PER_PAGE'], False)
    next_url = url_for('athlete.search', q=search, page=athletes.next_num) \
        if athletes.has_next else None
    prev_url = url_for('athlete.search', q=search, page=athletes.prev_num) \
        if athletes.has_prev else None
    return render_template('athlete/athletes.html', title=_('Search athletes'), athletes=athletes.items, 
        next_url=next_url, prev_url=prev_url, form=form)
        # , posts=posts, next_url=next_url, prev_url=prev_url)
