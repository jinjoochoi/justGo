from .models import TrafficType, PathSearchResult, PathSearchResultCode
from . import mongo
from .config.config import Config
from .models.Path import Path
from .util.util import convertToFriendlyTime 
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
         return self.searchPath(Path(source_id,route[0],destination_id,route[1]))
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
     return self.makePathMessage(path[0], option)


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
     #import pdb;pdb.set_trace()
     if res.status_code == requests.codes.ok:
       # location, totalTransitCount정보도 같이 저장합니다.
       location = {'source_id':path.source_id, 'source_name':path.source_name,'destination_id':path.destination_id,'destination_name':path.destination_name}
       paths = res.json()['result']['path']
       for p in paths:
          totalTransitCount = {'totalTransitCount': p['info']['busTransitCount'] + p['info']['subwayTransitCount']}
          mongo.db.paths.update({'mapObj': p['info']['mapObj']},
                                {'$set':{'pathType':p['pathType'],'subPath':p['subPath'],'info':p['info'],'location':location,'totalTransitCount':totalTransitCount}},upsert=True)  
       return PathSearchResult(PathSearchResultCode.SUCCESS,path)
     return PathSearchResult(PathSearchResultCode.NOTFOUND_PATH)


  """
      Make path message
    
  """

  def makePathMessage(self, path, option):
     message = ""
     message += self.makeIntroMessage(path,option)

     # 도보의 경우에는 startName과 endName의 정보가 없기 때문에 아래와 같이 구현했습니다.
     # i == first -> startName = path's source_name , endName = next subpath's startName
     # i == last -> startName = prev subpath's endName , endName = path's destination_name
     # else -> startName = prev subpath's endName, endName = next subpath's startName
     #import pdb; pdb.set_trace()
     for i in range(0,len(path['subPath'])):
        subpath = path['subPath'][i]
        if subpath['trafficType'] == TrafficType.WALK.value:
          source_name = ""
          destination_name = ""
          if i == 0:
            source_name = path['location']['source_name']
            destination_name = path['subPath'][i+1]['startName']
          elif i == len(path['subPath']) - 1 :
            source_name = path['subPath'][i-1]['endName']
            destination_name = path['location']['destination_name']
          else:
            source_name = path['subPath'][i-1]['endName'] 
            destination_name = path['subPath'][i+1]['startName'] 
          message += self.makeByWalkMessage(source_name,destination_name,subpath)
        elif subpath['trafficType'] == TrafficType.BUS.value:
          message += self.makeByBusMessage(subpath)
        elif subpath['trafficType'] == TrafficType.SUBWAY.value:
          message += self.makeBySubwayMessage(subpath)
     message += self.makePathInfoMessage(path['info'])
     return message

  def makeIntroMessage(self, path, option):
     source_name = path['location']['source_name'] 
     destination_name = path['location']['destination_name'] 
     return source_name +" ~ "+ destination_name + " "+option + '경로\n\n'

  #TODO: source, destination 추가
  def makeByWalkMessage(self, source_name, destination_name, subpath):
     return "[도보] " + source_name + " ~ "+ destination_name + '\n'

  #TODO: lane가 여러개일 경우
  def makeByBusMessage(self, subpath):
     return "["+ subpath['lane'][0]['busNo']+"번 버스] "+ subpath['startName']+" ~ "+subpath['endName'] + '\n'

  #TODO: lane가  여러개일 경우
  def makeBySubwayMessage(self, subpath):
     return "["+subpath['lane'][0]['name']+"]"+ subpath['startName']+" ~ "+subpath['endName'] + '\n'

  def makePathInfoMessage(self, info):
     return "총 요금 : "+str(info['payment'])+"원" + " 총 소요시간 : " + convertToFriendlyTime(info['totalTime'])+ '\n'

