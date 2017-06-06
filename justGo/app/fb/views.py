# -*- coding: utf-8 -*- 
from flask import Flask, request, Blueprint
from .. import PathManager,NLCManager, NLPManager, BusManager
from ..config.config import Config
from . import fb_messenger, FBMessengerManager
from ..models.NLPResult import NLPResultCode
from ..models.BusInfoSearchResult import BusInfoSearchResultCode


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
           FBMessengerManager.sendTypingOnAction(recipient_id)
           # quick_reply
           if x['message'].get('quick_reply'):
             quick_reply = x['message']['quick_reply']
             payload = quick_reply['payload']
             option = x['message']['text']
             message = PathManager.getPathMessage(payload,option)
             FBMessengerManager.sendTextMessage(recipient_id,message)
           # text     
           elif x['message'].get('text'):
             nlc_result = NLCManager.analysis(x['message']['text'])
             # NLC_CLASS : greeting
             if nlc_result == Config.NLC_CLASS_GREETING:
               FBMessengerManager.sendTextMessage(recipient_id,'안녕하세요.ㅎㅎ')
             # NLC_CLASS : ask name
             elif nlc_result == Config.NLC_CLASS_ASK_NAME:
               FBMessengerManager.sendTextMessage(recipient_id, '제 이름은 저스트고입니다.ㅎㅎ')
             # NLC_CLASS : slang
             elif nlc_result == Config.NLC_CLASS_SLANG:
               FBMessengerManager.sendTextMessage(recipient_id, '그러지말구 대중교통에 대해서 물어봐줄래요? :)')
             # NLC_CLASS : ask bus info
             elif nlc_result == Config.NLC_CLASS_BUS_INFO:
               nlp_result = NLPManager.findBusNo(x['message']['text'])
               if nlp_result.result_code == BusInfoSearchResultCode.UNSUPPORTED_FORMAT:
                 message = nlp_result.getErrorMessage()
               else:
                 result = BusManager.getBusInfo(nlp_result.bus_info)
                 if result.result_code == BusInfoSearchResultCode.NOTFOUND:
                   message = result.getErrorMessage()
                 else:
                   #FIXME : message가 너무 긴 경우 전송이 안됨.
                   message = BusManager.makeBusInfoMessage(result.bus_info)
               FBMessengerManager.sendTextMessage(recipient_id,message)
             # NLC_CLASS : ask path
             elif nlc_result == Config.NLC_CLASS_SEARCH_PATH:
               nlp_result = NLPManager.findSrcAndDest(x['message']['text'])
               if nlp_result.result_code == NLPResultCode.UNSUPPORTED_FORMAT:
                 FBMessengerManager.sendTextMessage(recipient_id,nlp_result.getErrorMessage())
               else:
                 result = PathManager.search(nlp_result.src, nlp_result.dest)
                 FBMessengerManager.sendReplyMessage(recipient_id, result)            
         else:
           pass
  return "Success"

