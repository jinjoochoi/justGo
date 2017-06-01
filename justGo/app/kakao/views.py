# -*- coding: utf-8 -*-
from flask import Flask, request, Blueprint, jsonify
from . import kakao_messenger
from .manager import APIHandler
from app import app

@kakao_messenger.route("/keyboard", methods=["GET", "POST"])
def yellow_keyboard():
    message, code = APIHandler.process("home")
    return jsonify(message), code
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
           kakao_messenger.sendTypingOnAction(recipient_id)
           # quick_reply
           if x['message'].get('quick_reply'):
             quick_reply = x['message']['quick_reply']
             payload = quick_reply['payload']
             option = x['message']['text']
             message = PathManager.getPathMessage(payload,option)
             kakao_messenger.sendTextMessage(recipient_id,message)
           # text     
           elif x['message'].get('text'):
             message = x['message']['text']
             result = PathManager.search(message)
             kakao_messenger.sendReplyMessage(recipient_id, result)            
         else:
           pass
  return "Success"
@kakao_messenger.route("/keyboard", methods=["GET"])
def yellow_message():
    message, code = APIHandler.process("message", request.json)
    return jsonify(message), code


@app.route("/friend", methods=["POST"]
def yellow_friend_add():
    message, code = APIHandler.process("add", request.json)
    return jsonify(message), code

@app.route("/friend/<key>", methods=["DELETE"])
def yellow_friend_block(key):
    message, code = APIHandler.process("block", key)
    return jsonify(message), code

@app.route("/chat_room/<key>", methods=["DELETE"])
def yellow_exit(key):
    message, code = APIHandler.process("exit", key)
    return jsonify(message), code
