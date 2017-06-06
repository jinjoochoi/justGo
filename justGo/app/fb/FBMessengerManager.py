from pymessenger.bot import Bot
from ..config.config import Config
from ..models.PathSearchResult import PathSearchResultCode

bot = Bot(Config.PAGE_ACCESS_TOKEN)

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance

class FBMessengerManager(metaclass=Singleton):

  def sendReplyMessage(self,recipient_id, result):
     if result.result_code == PathSearchResultCode.SUCCESS:
       self.sendSuggestionsReply(recipient_id,result)
     else:
       self.sendTextMessage(recipient_id, result.getErrorMessage())

  def sendTextMessage(self, recipient_id, message):
     bot.send_text_message(recipient_id, message)

  def sendSuggestionsReply(self,recipient_id,result):
     payload = str(result.path.source_id) + "," + str(result.path.destination_id) 
     bot.send_message(recipient_id,{
        "text":"어떤 우선순위를 기준으로 검색할까요?",
        "quick_replies": [
        {
            "content_type":"text",
            "title":Config.OPTION_SHORTEST_PATH,
            "payload":payload
            
        },
        {
            "content_type":"text",
            "title":Config.OPTION_LEAST_COST,
            "payload":payload
        },
        {
            "content_type":"text",
            "title":Config.OPTION_MINIMUM_TRANSFER,
            "payload":payload
        }
        ]
     }) 

  def sendTypingOnAction(self, recipient_id):
     bot.send_action(recipient_id, "typing_on")
     


