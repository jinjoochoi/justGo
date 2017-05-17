"""
from .. import db 
from marshmallow import Schema, fields
from sqlalchemy.ext.declarative import declarative_base 
from .Lane import LaneSchema
from .Station import StationSchema

Model, Column, Table, Integer, String, ForeignKey, relationship = db.Model, db.Column, db.Table, db.Integer, db.String, db.ForeignKey, db.relationship

# Association Table
Base = declarative_base()
subpaths_lanes = Table(
  "subpaths_lanes",
  Base.metadata,
  Column("subpathId", Integer, ForeignKey("subpath.id")),
  Column("laneId", Integer, ForeignKey("lane.id")),
)

subpaths_passStations = Table(
  "subpaths_passStations",
  Base.metadata,
  Column("subpathId", Integer, ForeignKey("subpath.id")),
  Column("stationId", Integer, ForeignKey("station.id")),
)
     
class SubPath(Model):
  __tablename__ = 'subpath'

  id = Column(Integer, primary_key = True, default=lambda: uuid.uuid4().hex)
  trafficType = Column(Integer)
  distance = Column(Integer)
  stationCount = Column(Integer) 
  wayCode = Column(Integer)

 ### Relation ###
  # Many To Many Relation with Lane
  lanes = relationship('Lane', secondary=lambda:'subpaths_lanes')
  # Many To Many Relation with Station
  passStations = relationship('Station', secondary=lambda:'subpaths_passStations') 
 
 
class Schema(Schema):
  id = fields.Int(dump_only=True)
  trafficType = fields.Int()
  distance = fields.Int()
  stationCount = fields.Int()
  wayCode = fields.Int()
  lanes = fields.Nested(LaneSchema, many=True)
  passStations = fields.Nested(StationSchema, many=True)
"""
