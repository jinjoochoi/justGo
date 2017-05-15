from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from .config.config import Config
import requests
import pdb

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
  db.init_app(app)

  # Create app blueprints
  from .bot import fb_messenger as fb_messenger_blueprint
  app.register_blueprint(fb_messenger_blueprint, url_prefix='/webhook')
  return app
