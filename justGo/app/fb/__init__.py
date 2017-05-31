from flask import Blueprint
from .FBMessengerManager import FBMessengerManager

fb_messenger = Blueprint('fb_messenger', __name__)
FBMessengerManager = FBMessengerManager()

from . import views
