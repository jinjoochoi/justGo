# -*- coding: utf-8 -*-
from flask import Flask, request, Blueprint, jsonify
from . import kakao_messenger
from .manager import APIHandler

@kakao_messenger.route("/keyboard", methods=["GET"])
def yellow_keyboard():
    #message, code = APIHandler.process("home")
    code = 200
    message = {"type": "text"} 
    return jsonify(message), code

@kakao_messenger.route("/message", methods=["GET", "POST"])
def yellow_message():
    message, code = APIHandler.process("message", request.json)
    return jsonify(message), code

@kakao_messenger.route("/friend", methods=["POST"])
def yellow_friend_add():
    message, code = APIHandler.process("add", request.json)
    return jsonify(message), code

@kakao_messenger.route("/friend/<key>", methods=["DELETE"])
def yellow_friend_block(key):
    message, code = APIHandler.process("block", key)
    return jsonify(message), code

@kakao_messenger.route("/chat_room/<key>", methods=["DELETE"])
def yellow_exit(key):
    message, code = APIHandler.process("exit", key)
    return jsonify(message), code
