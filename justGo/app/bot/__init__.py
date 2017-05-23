from flask import Blueprint
from .BotManager import BotManager

bot = Blueprint('bot',__name__)
BotManager = BotManager()

from . import views
