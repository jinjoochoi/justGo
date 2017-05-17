from flask import Flask, request
from flask_pymongo import PyMongo
from .config.config import Config
import requests
import pdb

mongo = PyMongo(config_prefix='MONGO')

def create_app():
  app = Flask(__name__)
  app.config['MONGO_DBNAME'] = Config.MONGO_DBNAME
  app.config['MONGO_URI'] = Config.MONGO_URI 
  mongo.init_app(app)
  # Create app blueprints
  from .bot import fb_messenger as fb_messenger_blueprint
  app.register_blueprint(fb_messenger_blueprint, url_prefix='/webhook')
  return app


