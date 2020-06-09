from app import create_app, db
from app.models import User, Athlete, Apparel, Event, Group, TargetResults, \
					   Role, Permission

app = create_app()

# useful in 'flask shell' to not import it everytime
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Athlete': Athlete, 'Apparel': Apparel, 'Event': Event, 'Group': Group, \
			'TargetResults': TargetResults, 'Role': Role, 'Permission': Permission}

