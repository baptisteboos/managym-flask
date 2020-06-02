from app import app, db
from app.models import User, Player, Apparel, Event

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Player': Player, 'Apparel': Apparel, 'Event': Event}
