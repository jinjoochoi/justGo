from flask import Flask, request
from flask_pymongo import PyMongo
from .config.config import Config
import requests
import pdb

mongo = PyMongo(config_prefix='MONGO')
from .PathManager import PathManager
PathManager = PathManager()
from .NLCManager import NLCManager
NLCManager = NLCManager()

def create_app():
  app = Flask(__name__)
  app.config['MONGO_DBNAME'] = Config.MONGO_DBNAME
  app.config['MONGO_URI'] = Config.MONGO_URI 
  mongo.init_app(app)
  # Create app blueprints
  from .fb import fb_messenger as fb_messenger_blueprint
  from .kakao import kakao_messenger as kakao_messenger_blueprint
  from .bot import bot as bot_blueprint
  app.register_blueprint(fb_messenger_blueprint, url_prefix='/webhook')
  app.register_blueprint(bot_blueprint, url_prefix='/bot')
  app.register_blueprint(kakao_messenger_blueprint, url_prefix='')
  return app


