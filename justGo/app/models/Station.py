from marshmallow import Schema, fields
from .. import db

Model, Column, Integer, String, Float= db.Model, db.Column, db.Integer, db.String, db.Float

class Station(Model):
  __tablename__ = "station"

  id = Column(Integer, primary_key=True)
  name = String(String(20))
  lat = Column(Float())
  lng = Column(Float())

class StationSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str()
  lat = fields.Float()
  lng = fields.Float()
