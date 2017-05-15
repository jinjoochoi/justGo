from .. import db
from marshmallow import Schema, fields

Model, Column, Integer, String =  db.Model, db.Column, db.Integer, db.String

class Lane(Model):
  __tablename__ = 'lane'
  
  subwayCode = Column(Integer, primary_key = True)
  name = Column(String(20))
  subwayCityCode = Column(Integer)

class LaneSchema(Schema):
  subwayCode = fields.Int(dump_only=True)
  name = fields.Str()
  subwayCityCode = fields.Int()
  
