from .. import db
from marshmallow import Schema, fields, post_load
import pdb

Model, Column, Integer, Float, String, relation = db.Model, db.Column, db.Integer, db.Float, db.String, db.relation

class Location(object):
  address = "" 
  lat, lng = 0

  def __init__(self, address, lat, lng):
     self.address = address
     self.lat = lat
     self.lng = lng
   
