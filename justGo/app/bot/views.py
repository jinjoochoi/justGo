# -*- coding: utf-8 -*- 
from flask import Flask, request, Blueprint
from pymessenger.bot import Bot
from .. import db
from ..models.Location import Location, LocationSchema
from ..models.Path import Path, PathSchema
from ..config.config import Config
from . import fb_messenger
import requests
import json
import pdb

bot = Bot(Config.PAGE_ACCESS_TOKEN)
locationSchema = LocationSchema()
pathSchema = PathSchema(many=True)


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
       searchPath(source,destination)
     else:
       message = "입력해주신 위치를 찾지못했어요. 정확하게 입력해주세요. :)"
       sendTextMessage(recipient_id,message)
   else:
     message = "지원하지 않는 형식의 텍스트입니다. '강남역 홍대입구역'와 같은 형식으로 입력해주세요! :)"
     sendTextMessage(recipient_id, message)

def searchPath(source, destination):
   params = {'svcID' : Config.AROINTECH_SVCID, 'OPT' : 0, 
             'SX' : source.data['lng'], 'SY' : source.data['lat'],
             'EX' : destination.data['lng'], 'EY' : destination.data['lat'],
             'output' : 'json', 'Lang' : 0 , 'resultCount' : 10}        
   res = requests.get(Config.AROINTECH_URL, params = params)
   if res.status_code == requests.codes.ok:
     results = res.json()['result']['path']
     #paths = []
     paths = pathSchema.loads(json.dumps(results))
     """
     for i in range(0, len(results)):
       paths.append(pathSchema(results[i]))
     """
     db.session.add(paths)
     db.session.commit()
     return paths[0]
   return None

def checkMessageFormat(message):
   return len(message.split(" ")) == 2

def getLocation(address):
   params = {'address' : address , 'key' : Config.GOOGLE_MAPS_API_KEY}
   res = requests.get(Config.GOOGLE_MAPS_URL, params = params)
   if res.status_code == requests.codes.ok:
     result = res.json()['results'][0]['geometry']['location']
     pdb.set_trace()
     location = locationSchema.loads(json.dumps(result))
     location.setAddress(address)
     db.session.add(location)
     db.session.commit()
     return location
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

