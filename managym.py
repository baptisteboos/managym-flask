from app import create_app, db
from app.models import User, Athlete, Apparatus, Event, Group, TargetResults, \
					   Role, Permission, Information, TypeInformation, AthleteEvent

app = create_app()

# useful in 'flask shell' to not import it everytime
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Athlete': Athlete, 'Apparatus': Apparatus, 'Event': Event, 'Group': Group, \
			'TargetResults': TargetResults, 'Role': Role, 'Permission': Permission, 'Information': Information, \
			'TypeInformation': TypeInformation, 'AthleteEvent': AthleteEvent}

