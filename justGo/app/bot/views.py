# -*- coding: utf-8 -*-
from flask import Flask, request, Blueprint, jsonify
from . import bot, BotManager
from .. import PathManager, NLCManager, NLPManager, BusManager
from ..config.config import Config 
from ..models.NLPResult import NLPResultCode
from ..models.BusInfoSearchResult import BusInfoSearchResultCode

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
        # NLC_CLASS : greeting
        if nlc_result == Config.NLC_CLASS_GREETING:
          message = '안녕하세요.ㅎㅎ'
          return jsonify(result = message)
        # NLC_CLASS : ask name
        elif nlc_result == Config.NLC_CLASS_ASK_NAME:
          message = '제 이름은 저스트고입니다.ㅎㅎ'
          return jsonify(result = message)
        # NLC_CLASS : slang
        elif nlc_result == Config.NLC_CLASS_SLANG:
          message = '그러지말구 대중교통에 대해서 물어봐줄래요? :)' 
          return jsonify(result = message)
        # NLC_CLASS : ask bus info
        elif nlc_result == Config.NLC_CLASS_BUS_INFO:
          nlp_result = NLPManager.findBusNo(output['messaging']['text'])
          if nlp_result.result_code == BusInfoSearchResultCode.UNSUPPORTED_FORMAT:
            message = nlp_result.getErrorMessage()
            return jsonify(result = message)
          else:
            result = BusManager.getBusInfo(nlp_result.bus_info)
            if result.result_code == BusInfoSearchResultCode.NOTFOUND:
              message = result.getErrorMessage()
              return jsonify(result = message)
            else:
              message = BusManager.makeBusInfoMessage(result.bus_info)
              return jsonify(result = message)
        # NLC_CLASS : ask path 
        elif nlc_result == Config.NLC_CLASS_SEARCH_PATH:
          nlp_result = NLPManager.findSrcAndDest(output['messaging']['text'])
          if nlp_result.result_code == NLPResultCode.UNSUPPORTED_FORMAT:
            message = nlp_result.getErrorMessage()
            return jsonify(result = message)
          else:
            result = PathManager.search(nlp_result.src, nlp_result.dest)
            message = BotManager.sendReplyMessage(result)
            return jsonify(result = message)
