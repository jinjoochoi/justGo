# -*- coding: utf-8 -*-
from flask import Flask, request, Blueprint, jsonify
from . import kakao_messenger

@kakao_messenger.route("/keyboard", methods=["GET"])
def yellow_keyboard():
   message = {"type" : "buttons","buttons" : ["선택 1", "선택 2", "선택 3"]} 
   code = 200
   return jsonify(message),code

@kakao_messenger.route("/message", methods=["POST"])
def yellow_message():
   message = {"type" : "buttons","buttons" : ["선택 1", "선택 2", "선택 3"]} 
   code = 200
   return jsonify(message),code

@kakao_messenger.route("/friend", methods=["POST"])
def yellow_friend():
   message = {"type" : "buttons","buttons" : ["선택 1", "선택 2", "선택 3"]} 
   code = 200
   return jsonify(message),code

@kakao_messenger.route("/friend/<key>", methods=["DELETE"])
def yellow_friend_block(key):
   message = {"type" : "buttons","buttons" : ["선택 1", "선택 2", "선택 3"]} 
   code = 200
   return jsonify(message),code

@kakao_messenger.route("/chat_room/<key>", methods=["DELETE"])
def yellow_exit(key):
   message = {"type" : "buttons","buttons" : ["선택 1", "선택 2", "선택 3"]} 
   code = 200
   return jsonify(message),code
