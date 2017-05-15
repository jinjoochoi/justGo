from .. import db
from marshmallow import Schema, fields, post_load
#from .Path import PathSchema 

Model, Column, Integer, Float, String, relation = db.Model, db.Column, db.Integer, db.Float, db.String, db.relation

class Location(Model):
  __tablename__ = 'location'

  id = Column(Integer, primary_key = True, default=lambda: uuid.uuid4().hex)
  address = Column(String(50), unique = True)
  lat = Column(Float)
  lng = Column(Float)

  # One To Many relation with Path 
  #paths = relation("Path")
  #stationId = Column(Integer)

  def __init__(self, lat, lng):
     self.lat = lat
     self.lng = lng

  def setAddress(self, addr):
     self.address = addr

class LocationSchema(Schema):
  id = fields.Int(dump_only=True)
  address = fields.Str()
  lat = fields.Float()
  lng = fields.Float()
  #paths = fields.Nested(PathSchema, many=True)

  @post_load
  def make_object(self,data):
     return Location(lat=data['lat'],
                     lng=data['lng'])
   
