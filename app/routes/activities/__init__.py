from flask import Blueprint

bp = Blueprint('activities', __name__)

from .activities import response
