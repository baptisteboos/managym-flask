from app import create_app, db
from app.models import User, Player, Apparel, Event

app = create_app()

# useful in 'flask shell' to not import it everytime
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Player': Player, 'Apparel': Apparel, 'Event': Event}
