from flask import Blueprint

bp = Blueprint('athlete', __name__)

from app.athlete import routes