# -*- coding: utf-8 -*-
from .message import * 
from ..models.PathSearchResult import PathSearchResultCode

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
        print(options.get(mode)(*args))
        message = {"message":{"text" : "귀하의 차량이 성공적으로 등록되었습니다. 축하합니다!"}}
        #message = options.get(mode)(*args)
        response_code = 200
        return message, response_code
        """
        try:
        except:
            message = self.handle_fail()
            response_code = 400
            return message, response_code
        """


    def return_home_message(self):
        message = MessageHandler.get_home_message()
        print(message)
        return message

    def handle_message(self, data):
        """
        [POST] your_server_url/message 일 때 사용되며
        사용자가 전달한 data에 따라 처리 과정을 거쳐 메시지를 반환하는 메인 함수입니다.
        """
        user_key = data["user_key"]
        request_type = data["type"]
        content = data["content"]
        nlc_result = NLCManager.analysis(content)
        if nlc_result == Config.NLC_CLASS_GREETING:
          message = MessageHandler.get_greeting_message()
        elif nlc_result == Config.NLC_CLASS_SEARCH_PATH:
          nlp_result = NLPManager.findSrcAndDest(content)
          result = PathManager.search(nlp_result)
          if result.result_code == PathSearchResultCode.SUCCESS:
            return MessageHandler.get_suggestions_message()
          else:
            return MessageHandler.get_path_search_fail_message(result)
            
        return message

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


class MessageManager(metaclass=Singleton):
    def get_base_message(self):
        base_message = BaseMessage().get_message()
        return base_message

    def get_greeting_message(self):
        greeting_message = GreetingMessage().get_message()
        return greeting_message

    def get_SuggestionsReply(self):
        suggestions_message = SuggestionsMessage().get_message()
        return suggestions_message

    def get_home_message(self):
        home_message = HomeMessage().get_message()
        return home_message

    def get_path_search_fail_message(self, result):
        fail_message = PathSearchMessage(result).get_message()
        return fail_message 

    def get_fail_message(self):
        fail_message = FailMessage().get_message()
        return fail_message

    def get_success_message(self):
        success_message = SuccessMessage().get_message()
        return success_message

APIHandler = APIManager()
MessageHandler = MessageManager()
