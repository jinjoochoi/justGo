import requests
from .config.config import Config
from .models.BusInfoSearchResult import *

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance

class BusManager(metaclass=Singleton):

  def getBusInfo(self, busNo):
     params = {'svcID' : Config.AROINTECH_SVCID, 'busNo' : busNo, 'output' : 'json' }
     print(busNo)
     res = requests.get(Config.AROINTECH_URL_BUS_INFO, params = params)
     if res.status_code == requests.codes.ok and not res.json()['result'] is None :
       return BusInfoSearchResult(BusInfoSearchResultCode.SUCCESS, res.json()['result']['lane'])
     return BusInfoSearchResult(BusInfoSearchResultCode.NOTFOUND)
  
  def makeBusInfoMessage(self, bus_info):
     message = ""
     for lane in bus_info:
       message += "["+lane['busCityName']+" "+lane['busNo']+"]\n기점: "+lane['busStartPoint']+"\n종점: "+lane['busEndPoint']+"\n"+"첫차시간: "+lane['busFirstTime']+"\n"+"막차시간: "+lane['busLastTime']+"\n\n"

     return message
