from konlpy.tag import Mecab
from .models.NLPResult import NLPResult, NLPResultCode

class Singleton(type):                                                         
  instance = None                                                              
                                                                               
  def __call__(cls, *args, **kwargs):                                          
    if not cls.instance:                                                       
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)           
    return cls.instance                                                        

class NLPManager(metaclass=Singleton):
  mecab = Mecab()
  
 #TODO : need to advance
  def findSrcAndDest(self, message):
    print(message)
    nouns = self.mecab.nouns(message)  
    if nouns is None or len(nouns) < 2:
      return NLPResult(NLPResultCode.UNSUPPORTED_FORMAT)
    return NLPResult(NLPResultCode.SUCCESS,nouns[0], nouns[1])
