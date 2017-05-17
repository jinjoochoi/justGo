from .models import TrafficType, PathSearchResult, PathSearchResultCode
from . import mongo
from .config.config import Config
import requests
import json

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance


class PathManager(metaclass=Singleton):
  def makeReplyMessage(self, message):
     if self.checkMessageFormat(message):
       route = message.split(" ")
       source = self.getLocation(route[0])
       destination = self.getLocation(route[1])
       if source != None and destination != None:
         path_id = self.searchPath(source,destination)
         if path_id != None:
           #paths = mongo.db.paths.find_one({"_id":path_id})
           return PathSearchResult(PathSearchResultCode.SUCCESS, path_id) 
         else:
           return PathSearchResult(PathSearchResultCode.NOTFOUND_PATH)
       else:
         return PathSearchResult(PathSearchResultCode.NOTFOUND_LOCATION) 
     else:
       return PathSearchResult(PathSearchResultCode.UNSUPPORTED_FORMAT)

  def checkMessageFormat(self, message):
     return len(message.split(" ")) == 2

  def getLocation(self, address):
     params = {'address' : address , 'key' : Config.GOOGLE_MAPS_API_KEY}
     res = requests.get(Config.GOOGLE_MAPS_URL, params = params)
     if res.status_code == requests.codes.ok:
       return res.json()['results'][0]['geometry']['location']
     else:
       return None

  def searchPath(self, source, destination):
     params = {'svcID' : Config.AROINTECH_SVCID, 'OPT' : 0,
               'SX' : source['lng'], 'SY' : source['lat'],
               'EX' : destination['lng'], 'EY' : destination['lat'],
               'output' : 'json', 'Lang' : 0 , 'resultCount' : 10}
     res = requests.get(Config.AROINTECH_URL, params = params)
     if res.status_code == requests.codes.ok:
       result = res.json()['result']
       location = {'source':source, 'destination':destination}
       result.update(location) # location정보도 같이 저장합니다.
       paths = mongo.db.paths
       path_id = paths.insert(result)
       return path_id
     return None



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

  def sendPathMessage(self, paths):
     path = paths['path'][0]
     message = ""
     for i in range(len(path['subPath'])):
        subpath = path['subPath'][i]
        if subpath['trafficType'] == TrafficType.WALK.value:
          message += makeByWalkMessage(subpath)
        elif subpath['trafficType'] == TrafficType.BUS.value:
          message += makeByBusMessage(subpath)
        elif subpath['trafficType'] == TrafficType.SUBWAY.value:
          message += makeBySubwayMessage(subpath)
     message += makePathInfoMessage(path['info'])
     return message

