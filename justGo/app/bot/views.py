# -*- coding: utf-8 -*-
from flask import Flask, request, Blueprint, jsonify
from . import bot, BotManager
from .. import PathManager,NLCManager,NLPManager
from ..config.config import Config 

@bot.route('/', methods=['POST'])
def webbhook():
   if request.method == 'POST':
     output = request.get_json()
     if output['messaging'].get('quick_reply'):
        option = output['messaging']['quick_reply']['option']
        payload = output['messaging']['quick_reply']['payload']
        message = PathManager.getPathMessage(payload,option)
        return jsonify(result = message)
     elif output['messaging'].get('text'):
        nlc_result = NLCManager.analysis(output['messaging']['text'])
        if nlc_result == Config.NLC_CLASS_GREETING:
          message = '안녕하세요.ㅎㅎ'
          return jsonify(result = message)
        elif nlc_result == Config.NLC_CLASS_ASK_NAME:
          message = '제 이름은 저스트고입니다.ㅎㅎ'
          return jsonify(result = message)
        elif nlc_result == Config.NLC_CLASS_SLANG:
          message = '그러지말구 대중교통에 대해서 물어봐줄래요? :)' 
          return jsonify(result = message)
        elif nlc_result == Config.NLC_CLASS_SEARCH_PATH:
          nlp_result = NLPManager.findSrcAndDest(output['messaging']['text'])
          if nlp_result.result_code == NLPResultCode.UNSUPPORTED_FORMAT:
            message = nlp_result.getErrorMessage()
            return jsonify(result = message)
          else:
            result = PathManager.search(nlp_result)
            message = BotManager.sendReplyMessage(result)
            return jsonify(result = message)
