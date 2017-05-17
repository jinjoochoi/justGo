# -*- coding: utf-8 -*- 
from flask import Flask, request, Blueprint
from pymessenger.bot import Bot
from .. import mongo
from ..config.config import Config
from . import fb_messenger
from ..models.TrafficType import TrafficType 
import requests
import json
import pdb

bot = Bot(Config.PAGE_ACCESS_TOKEN)

@fb_messenger.route('', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    if request.args.get("hub.verify_token") == Config.VALIDATION_TOKEN:
      return request.args.get("hub.challenge") 
    else:
      return 'Invalid verification token'
  if request.method == 'POST':
    output = request.get_json()
    for event in output['entry']:
       messaging = event['messaging']
       for x in messaging:
         if x.get('message'):
           recipient_id = x['sender']['id'] 
           if x['message'].get('text'):
             message = x['message']['text']
             receivedMessage(recipient_id, message)
         else:
           pass
  return "Success"

def receivedMessage(recipient_id, message):
   if checkMessageFormat(message):
     route = message.split(" ")
     source = getLocation(route[0])
     destination = getLocation(route[1])
     if source != None and destination != None:
       path_id = searchPath(source,destination)
       if path_id != None:
         paths = mongo.db.paths.find_one({"_id":path_id})
         sendPathMessage(recipient_id, paths)
     else:
       message = "입력해주신 위치를 찾지못했어요. 정확하게 입력해주세요. :)"
       sendTextMessage(recipient_id,message)
   else:
     message = "지원하지 않는 형식의 텍스트입니다. '강남역 홍대입구역'와 같은 형식으로 입력해주세요! :)"
     sendTextMessage(recipient_id, message)

#TODO: source, destination 추가 
def makeByWalkMessage(subpath):
   return "[도보] "

#TODO: lane가 여러개일 경우 
def makeByBusMessage(subpath):
   return "["+ subpath['lane'][0]['busNo']+"번 버스]"+ subpath['startName']+" ~ "+subpath['endName']

#TODO: lane가  여러개일 경우  
def makeBySubwayMessage(subpath):
   return "["+subpath['lane'][0]['name']+"]"+ subpath['startName']+" ~ "+subpath['endName']
   
def sendPathMessage(recipient_id, paths):
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
   sendTextMessage(recipient_id, message)

def makePathInfoMessage(info):
   return "총 요금 : "+str(info['payment']) + "총 소요시간 : " + str(info['totalTime'])

def searchPath(source, destination):
   params = {'svcID' : Config.AROINTECH_SVCID, 'OPT' : 0, 
             'SX' : source['lng'], 'SY' : source['lat'],
             'EX' : destination['lng'], 'EY' : destination['lat'],
             'output' : 'json', 'Lang' : 0 , 'resultCount' : 10}        
   res = requests.get(Config.AROINTECH_URL, params = params)
   if res.status_code == requests.codes.ok:
     result = res.json()['result']
     location = {'source':source, 'destination':destination}
     result.update(location)
     paths = mongo.db.paths
     path_id = paths.insert(result)
     return path_id
   return None

def checkMessageFormat(message):
   return len(message.split(" ")) == 2

def getLocation(address):
   params = {'address' : address , 'key' : Config.GOOGLE_MAPS_API_KEY}
   res = requests.get(Config.GOOGLE_MAPS_URL, params = params)
   if res.status_code == requests.codes.ok:
     return res.json()['results'][0]['geometry']['location']
   else:
     return None

def sendTextMessage(recipient_id, message):
   bot.send_text_message(recipient_id, message)
    
def sendSuggestionsReply(recipient_id):
   bot.send_message(recipient_id,{
        "text":"원하는 정보가 무엇인가요?",
        "quick_replies": [
        {
            "content_type":"text",
            "title":"최단경로",
            "payload":Config.PAYLOAD_QUICK_REPLY_SUGGESTIONS_SHORTEST_PATH
        },
        {
            "content_type":"text",
            "title":"최소비용경로",
            "payload":Config.PAYLOAD_QUICK_REPLY_SUGGESTIONS_LEAST_COST
        },
        {
            "content_type":"text",
            "title":"최소환승경로",
            "payload":Config.PAYLOAD_QUICK_REPLY_SUGGESTIONS_MINIMUM_TRANSFER
        }
        ]
   })

