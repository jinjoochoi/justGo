# -*- coding: utf-8 -*-
from .keyboard import Keyboard
from ..config.config import Config
from ..models.PathSearchResult import PathSearchResultCode
from ujson import dumps, loads


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)

class Message:

    """
    반환될 메시지들의 추상 클래스입니다.
    별도의 수정은 필요하지 않습니다.
    본 클래스에 포함되어 있는 dict타입의 변수들은 조합을 위한 조각과 틀입니다.
    :param dict base_keyboard: 키보드
    :param dict base_message: 키보드를 포함한 기본 메시지
    :param dict base_message_button: 메시지에 덧붙여질 메시지버튼
    """
    _base_keyboard = {
        "type": "buttons",
        "buttons": []
    }
    _base_message = {
        "message": {
            "text": "원하는 정보가 무엇인가요?",
        }
    }
    _base_message_button = {
        "message_button": {
            "label": "홈버튼",
            "url": "http://pf.kakao.com/_xilUHd",
        },
    }
    _base_photo = {
        "photo": {
            "url": "http://k.kakaocdn.net/dn/bCvwU7/btqgGIq49ed/x4brYXsTcdMkBuZpXTK7b0/img_m.jpg",
            "width": 640,
            "height": 480,
        },
    }

    def __init__(self):
        self.returned_message = None

    def get_message(self):
        return self.returned_message

    @classproperty
    def base_keyboard(cls):
        return loads(dumps(cls._base_keyboard))

    @classproperty
    def base_message(cls):
        return loads(dumps(cls._base_message))

    @classproperty
    def base_message_button(cls):
        return loads(dumps(cls._base_message_button))

    @classproperty
    def base_photo(cls):
        return loads(dumps(cls._base_photo))

    def sendReplyMessage(self, data, result):
     if result.result_code == PathSearchResultCode.SUCCESS:
       self.sendSuggestionsReply(data,result)
     else:
       self.sendTextMessage(data, result.getErrorMessage())


class BaseMessage(Message):
    def __init__(self):
        super().__init__()
        self.returned_message = Message.base_message


    def remove_keyboard(self):
        """
        반환될 메시지에서 키보드를 삭제합니다.
        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.remove_keyboard()
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지"
                }
            }
        """
        if "keyboard" in self.returned_message:
            del self.returned_message["keyboard"]

    def add_photo(self, url, width, height):
        """
        반환될 메시지에 사진을 추가합니다.
        :param str url: 사진이 위치해 있는 URL
        :param int width: 사진의 가로 길이
        :param int height: 사진의 세로 길이
        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> url = "https://www.python.org/static/img/python-logo.png"
            >>> a.add_photo(url, 400, 400)
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지",
                    "photo": {
                        "url": "https://www.python.org/static/img/python-logo.png",
                        "width": 400,
                        "height": 400,
                    }
                },
                "keyboard": 생략
            }
        """
        photo_message = Message.base_photo
        photo_message["photo"]["url"] = url
        photo_message["photo"]["width"] = width
        photo_message["photo"]["height"] = height
        self.returned_message["message"].update(photo_message)

    def add_message_button(self, url, label):
        """
        반환될 메시지에 메시지버튼을 추가합니다.
        :param str url: 메시지버튼을 누르면 이동할 URL
        :param str label: 메시지버튼에 안내되는 메시지
        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.add_message_button("https://www.python.org", "파이썬")
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지",
                    "message_button": {
                        "label": "파이썬",
                        "url": "https://www.python.org"
                    }
                },
                "keyboard": 생략
            }
        """
        button_message = Message.base_message_button
        button_message["message_button"]["label"] = label
        button_message["message_button"]["url"] = url
        self.returned_message["message"].update(button_message)

    def update_message(self, message):
        self.returned_message["message"]["text"] = message

    def update_keyboard(self, keyboard):
        _keyboard = Message.base_keyboard
        _keyboard["buttons"] = keyboard
        self.returned_message["keyboard"] = _keyboard


class FailMessage(BaseMessage):
    """
    처리 중 예외가 발생했을 때 반환되는 메시지입니다.
    오류 메시지는 수정 가능하며 별도의 처리 로직을 추가하실 수 있습니다.
    """
    def __init__(self):
        super().__init__()
        self.update_message("오류가 발생하였습니다.")
        self.update_keyboard(Keyboard.home_buttons)

class SuggestionsMessage(BaseMessage):
   def __init__(self):
      super().__init__()
      self.update_message("어떤 우선순위를 기준으로 검색할까요?")
      self.update_keyboard(["최단거리","최소비용", "최소환승"])

class GreetingMessage(BaseMessage):
   def __init__(self):
       super().__init__()
       self.update_message("안녕ㅎㅎ")

class PathSearchFailMessage(BaseMessage):
   def __init__(self, result):
       super().__init__()
       self.update_message(result.getErrorMessage())

class HomeMessage(BaseMessage):
   def __init__(self):
       super().__init__()
       message = self._base_keyboard
       message['buttons'] = ["대화 시작하기"]
       self.returned_message = message 

class IntroMessage(BaseMessage):
   def __init__(self):
       super().__init__()
       message = self._base_message
       message['message']['text'] = "반가워요! 대중교통 경로검색이나\n첫차, 막차와 같은 정보를 물어보시면 친절하게 답해드릴게요 :)"
       self.returned_message = message 

class PathMessage(BaseMessage):
   def __init__(self, path_message):
       super().__init__()
       message = self._base_message
       message['message']['text'] = path_message
       self.returned_message = message 

class NameMessage(BaseMessage):
   def __init__(self):
       super().__init__()
       self.update_message("제 이름은 저스트고입니다.ㅎㅎ")

class SlangResponseMessage(BaseMessage):
   def __init__(self):
       super().__init__()
       self.update_message("그러지말구 대중교통에 대해서 물어봐줄래요? :)")

class BusInfoMessage(BaseMessage):
   def __init__(self, message):
       super().__init__()
       self.update_message(message)

class SuccessMessage(Message):
    """
    친구 추가, 차단, 채팅방 나가기가 발생했을 때 성공적으로 처리되면 반환되는 메시지입니다.
    """
    def __init__(self):
        super().__init__()
        self.returned_message = {"message": "SUCCESS", "comment": "정상 응답"}
