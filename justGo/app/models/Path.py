from .. import db
from marshmallow import Schema, fields
from sqlalchemy.ext.declarative import declarative_base

Model, Integer, String, Table, Column, ForeignKey, relationship = db.Model, db.Integer, db.String, db.Table, db.Column, db.ForeignKey, db.relationship

# Association Table
Base = declarative_base()
paths_subpaths = Table(
    "paths_subpaths",
    Base.metadata,
    Column("subpathId", Integer, ForeignKey("subpath.id")),
    Column("pathId", Integer, ForeignKey("path.id")),
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
  # Many To Many Relation with SubPath
  subPaths = relationship('subPath', secondary = paths_subpaths)

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
