from .. import db
from marshmallow import Schema, fields
from sqlalchemy.ext.declarative import declarative_base

Model, Integer, String, Table, Column, ForeignKey, relationship, backref= db.Model, db.Integer, db.String, db.Table, db.Column, db.ForeignKey, db.relationship, db.backref

# Association Table
Base = declarative_base()
paths_subpaths = Table(
    "paths_subpaths",
    Base.metadata,
    Column("subpathId", Integer, ForeignKey("Subpath.id")),
    Column("pathId", Integer, ForeignKey("Path.id")),
)

class Path(Model):
  __tablename__ = 'path'

  id = Column(Integer, primary_key = True, default=lambda: uuid.uuid4().hex)
  payment = Column(Integer)
  busTransitCount = Column(Integer) 
  subwayTransitCount = Column(Integer) 
  busStationCount = Column(Integer) 
  subwayStationCount = Column(Integer) 
  totalStationCount = Column(Integer) 
  totalTime = Column(Integer) 
  totalWalk = Column(Integer) 
  totalWalkTime = Column(Integer) 
  totalDistance = Column(Integer) 
  trafficDistance = Column(Integer) 
  firstStartStation = Column(String(30)) 
  lastEndStation = Column(String(30)) 

 ### Relation ###
  # One To Many Relation with Location
  sourceId = Column(Integer, ForeignKey('location.id'))
  destinationId = Column(Integer, ForeignKey('location.id'))
  source = relationship("Location", foreign_keys=[sourceId])
  destination = relationship("Location", foreign_keys=[destinationId])
  # Many To Many Relation with SubPath
  subPaths = relationship('SubPath', secondary = lambda:paths_subpaths, backref=backref('path', lazy='dynamic'))

  def setSourceId(self, sourceId):
    self.sourceId = sourceId

  def setDestinationId(self, destinationId):
    self.destinationId = destinationId

class PathSchema(Schema):
  id = fields.Int(dump_only=True)
  payment = fields.Int()
  busTransitCount = fields.Int()
  subwayTransitCount = fields.Int()
  busStationCount = fields.Int()
  subwayStationCount = fields.Int()
  totalStationCount = fields.Int()
  totalTime = fields.Int()
  totalWalk = fields.Int()
  totalWalkTime = fields.Int()
  totalDistance = fields.Int()
  trafficDistance = fields.Int()
  firstStartStation = fields.Str()
  lastEndStation = fields.Str()   
  
"""
  def getPathMessage(self, num):
    path = self.subPaths[num]
"""
from .Lane import LaneSchema
from .Station import StationSchema


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
