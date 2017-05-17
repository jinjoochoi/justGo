# -*- coding: utf-8 -*- 
from flask import Flask, request, Blueprint
from pymessenger.bot import Bot
from .. import mongo, PathManager
from ..config.config import Config
from . import fb_messenger, FBMessengerManager
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
            result = PathManager.makeReplyMessage(message)
            FBMessengerManager.sendReplyMessage(recipient_id, result)            
         else:
           pass
  return "Success"

