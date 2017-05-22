from .models import TrafficType, PathSearchResult, PathSearchResultCode
from . import mongo
from .config.config import Config
from .models.Path import Path
from bson import ObjectId
import requests
import json

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance


class PathManager(metaclass=Singleton):
  
  def search(self, message):
     if self.checkMessageFormat(message):
       route = message.split(" ")
       source_id = self.searchLocation(route[0])
       destination_id = self.searchLocation(route[1])
       if not source_id is None and  not destination_id is None:
         return self.searchPath(Path(source_id,destination_id))
       else:
         return PathSearchResult(PathSearchResultCode.NOTFOUND_LOCATION) 
     else:
       return PathSearchResult(PathSearchResultCode.UNSUPPORTED_FORMAT)

  def getPathMessage(self, payload, option):
     path = payload.split(',')
     source_id, destination_id = ObjectId(path[0]),ObjectId(path[1])
     if option == Config.OPTION_SHORTEST_PATH:
       path = mongo.db.paths.find({'location.source_id':source_id,'location.destination_id':destination_id}).sort([('info.totalTime',1)]).limit(1)
     elif option == Config.OPTION_LEAST_COST:
       path = mongo.db.paths.find({'location.source_id':source_id,'location.destination_id':destination_id}).sort([('info.totalDistance',1)])
     elif option == Config.OPTION_MINIMUM_TRANSFER:
       path = mongo.db.paths.find({'location.source_id':source_id,'location.destination_id':destination_id}).sort([('info.totalTransitCount',1)]).limit(1)
     return self.makePathMessage(path[0])

  def makePathMessage(self, path):
     message = ""
     for i in range(0,len(path['subPath'])):
        subpath = path['subPath'][i]
        if subpath['trafficType'] == TrafficType.WALK.value:
          message += self.makeByWalkMessage(subpath)
        elif subpath['trafficType'] == TrafficType.BUS.value:
          message += self.makeByBusMessage(subpath)
        elif subpath['trafficType'] == TrafficType.SUBWAY.value:
          message += self.makeBySubwayMessage(subpath)
     message += self.makePathInfoMessage(path['info'])
     return message


  def checkMessageFormat(self, message):
     return len(message.split(" ")) == 2

  def searchLocation(self, address):
     params = {'address' : address , 'key' : Config.GOOGLE_MAPS_API_KEY}
     res = requests.get(Config.GOOGLE_MAPS_URL, params = params)
     if res.status_code == requests.codes.ok:
       lat = res.json()['results'][0]['geometry']['location']['lat']
       lng = res.json()['results'][0]['geometry']['location']['lng']
       locations = mongo.db.locations
       result = locations.find_one({'lat':lat,'lng':lng})
       if result is None:
         result = locations.insert(res.json()['results'][0]['geometry']['location'])
         return result
       else:
         return result['_id']
     return None

  def searchPath(self, path):
     source = mongo.db.locations.find_one({'_id' : path.source_id})
     destination = mongo.db.locations.find_one({'_id' : path.destination_id})
     params = {'svcID' : Config.AROINTECH_SVCID, 'OPT' : 0,
               'SX' : source['lng'], 'SY' : source['lat'],
               'EX' : destination['lng'], 'EY' : destination['lat'],
               'output' : 'json', 'Lang' : 0 , 'resultCount' : 10}
     res = requests.get(Config.AROINTECH_URL, params = params)
     if res.status_code == requests.codes.ok:
       location = {'source_id':path.source_id, 'destination_id':path.destination_id}
       paths = res.json()['result']['path']
       for p in paths:
          totalTransitCount = {'totalTransitCount': p['info']['busTransitCount'] + p['info']['subwayTransitCount']}
          mongo.db.paths.update({'mapObj': p['info']['mapObj']},
                                {'$set':{'pathType':p['pathType'],'subPath':p['subPath'],'info':p['info'],'location':location,'totalTransitCount':totalTransitCount}},upsert=True)  
       return PathSearchResult(PathSearchResultCode.SUCCESS,path)
     return PathSearchResult(PathSearchResultCode.NOTFOUND_PATH)


  #TODO: source, destination 추가
  def makeByWalkMessage(self, subpath):
     return "[도보] "

  #TODO: lane가 여러개일 경우
  def makeByBusMessage(self, subpath):
     return "["+ subpath['lane'][0]['busNo']+"번 버스]"+ subpath['startName']+" ~ "+subpath['endName']

  #TODO: lane가  여러개일 경우
  def makeBySubwayMessage(self, subpath):
     return "["+subpath['lane'][0]['name']+"]"+ subpath['startName']+" ~ "+subpath['endName']
  def makePathInfoMessage(self, info):
     return "총 요금 : "+str(info['payment']) + "총 소요시간 : " + str(info['totalTime'])

