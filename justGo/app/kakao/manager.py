# -*- coding: utf-8 -*-
from .message import * 
from .. import mongo
from ..models.PathSearchResult import PathSearchResultCode
from .. import NLCManager, NLPManager, PathManager, BusManager
from ..models.BusInfoSearchResult import BusInfoSearchResultCode
from ..config.config import Config
from bson import ObjectId

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, mode, *args):
        options = {
             "home": self.return_home_message,
             "message": self.handle_message,
             "add": self.add_friend,
             "block": self.block_friend,
             "exit": self.exit_chatroom,
         }
        message = options.get(mode)(*args)
        response_code = 200
        return message, response_code

    def return_home_message(self):
        message = MessageHandler.get_home_message()
        return message


    def handle_message(self, data):
        user_key = data["user_key"]
        request_type = data["type"]
        content = data["content"]
        message = ""
        # intro message (/keyboard) 
        if content == '대화 시작하기' :
          message = MessageHandler.get_intro_message()
        # suggestions message
        elif content == '최단거리' or content == '최소비용' or content == '최소환승':
          kakao_context = self.get_kakao_context(user_key)
          payload = str(kakao_context['source_id']) + "," + str(kakao_context['destination_id'])
          path_message = PathManager.getPathMessage(payload, content)
          message = MessageHandler.get_path_message(path_message)
        else:
          nlc_result = NLCManager.analysis(content)
          # NLC_CLASS : greeting
          if nlc_result == Config.NLC_CLASS_GREETING:
            message = MessageHandler.get_greeting_message()
          # NLC_CLASS : ask name
          elif nlc_result == Config.NLC_CLASS_ASK_NAME:
            message = MessageHandler.get_name_message()
          # NLC_CLASS : slang
          elif nlc_result == Config.NLC_CLASS_SLANG:
            message = MessageHandler.get_slang_response_message()
          # NLC_CLASS : ask bus info
          elif nlc_result == Config.NLC_CLASS_BUS_INFO:
            nlp_result = NLPManager.findBusNo(content)
            if nlp_result.result_code == BusInfoSearchResultCode.UNSUPPORTED_FORMAT:
              message = MessageHandler.get_bus_info_message(nlp_result.getErrorMessage())
            else:
              result = BusManager.getBusInfo(nlp_result.bus_info)
              if result.result_code == BusInfoSearchResultCode.NOTFOUND:
                message = MessageHandler.get_bus_info_message(nlp_result.getErrorMessage())
              else:
                bus_message = BusManager.makeBusInfoMessage(result.bus_info)
                message = MessageHandler.get_bus_info_message(bus_message)
          # NLC_CLASS : ask path
          elif nlc_result == Config.NLC_CLASS_SEARCH_PATH:
            nlp_result = NLPManager.findSrcAndDest(content)
            result = PathManager.search(nlp_result.src, nlp_result.dest)
            if result.result_code == PathSearchResultCode.SUCCESS:
              self.update_kakao_context(user_key, result.path.source_id, result.path.destination_id)
              message = MessageHandler.get_suggestions_message()
            else:
              message = MessageHandler.get_path_search_fail_message(result)
            
        return message
 
    def get_kakao_context(self, user_key):
        return mongo.db.contexts.find_one({'user_key' : user_key})
       

    def update_kakao_context(self, user_key, source_id, destination_id):
        mongo.db.contexts.insert({'user_key' : user_key,'source_id' : source_id,'destination_id' : destination_id})
   
    def add_friend(self, data):
        """
        [POST] your_server_url/friend 일 때 사용되는 함수입니다.
        기본 동작으로 수집된 user_key를 DB에 추가합니다.
        """
        user_key = data["user_key"]
        message = MessageHandler.get_success_message()
        return message

    def block_friend(self, user_key):
        """
        [DELETE] your_server_url/friend/{user_key} 일 때 사용되는 함수입니다.
        기본 동작으로 수집된 user_key를 DB에서 제거합니다.
        """
        message = MessageHandler.get_success_message()
        return message

    def exit_chatroom(self, user_key):
        """
        [DELETE] your_server_url/chat_room/{user_key} 일 때 사용되는 함수입니다.
        """
        message = MessageHandler.get_success_message()
        return message

    def handle_fail(self):
        """
        처리 중 예외가 발생했을 때 사용되는 함수입니다.
        """
        message = MessageHandler.get_fail_message()
        return message


class MessageHandler(metaclass=Singleton):
    def get_base_message(self):
        base_message = BaseMessage().get_message()
        return base_message

    def get_greeting_message(self):
        greeting_message = GreetingMessage().get_message()
        return greeting_message

    def get_suggestions_message(self):
        suggestions_message = SuggestionsMessage().get_message()
        return suggestions_message

    def get_home_message(self):
        home_message = HomeMessage().get_message()
        return home_message

    def get_intro_message(self):
        intro_message = IntroMessage().get_message()
        return intro_message

    def get_path_message(self, path_message):
        path_message = PathMessage(path_message).get_message()
        return path_message

    def get_path_search_fail_message(self, result):
        fail_message = PathSearchMessage(result).get_message()
        return fail_message 

    def get_name_message(self):
        name_message = NameMessage().get_message()
        return name_message 

    def get_slang_response_message(self):
        slang_response_message = SlangResponseMessage().get_message()
        return slang_response_message 

    def get_bus_info_message(self, result):
        bus_info_message = BusInfoMessage(result).get_message()
        return bus_info_message 

    def get_fail_message(self):
        fail_message = FailMessage().get_message()
        return fail_message

    def get_success_message(self):
        success_message = SuccessMessage().get_message()
        return success_message

MessageHandler = MessageHandler()

