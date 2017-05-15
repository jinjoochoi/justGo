from flask import Blueprint

fb_messenger = Blueprint('fb_messenger', __name__)

from . import views
