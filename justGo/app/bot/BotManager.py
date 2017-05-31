from ..config.config import Config
from ..models.PathSearchResult import PathSearchResultCode

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance

class BotManager(metaclass=Singleton):

  def sendReplyMessage(self, result):
     if result.result_code == PathSearchResultCode.SUCCESS:
       return self.sendSuggestionsReply(result)
     else:
       err_message = result.getErrorMessage()
       return {"text": err_message}

  def sendSuggestionsReply(self,result):
     payload = str(result.path.source_id) + "," + str(result.path.destination_id)
     return { 
               "text":"원하는 정보가 무엇인가요?",
               "quick_replies":[
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
             }]
            }
