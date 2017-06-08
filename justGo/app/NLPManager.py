from konlpy.tag import Mecab
from .models.NLPResult import NLPResult, NLPResultCode
from .models.BusInfoSearchResult import BusInfoSearchResultCode, BusInfoSearchResult

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
    nouns = self.mecab.nouns(message)  
    print(nouns)
    if nouns is None or len(nouns) < 2:
      return NLPResult(NLPResultCode.UNSUPPORTED_FORMAT)
    return NLPResult(NLPResultCode.SUCCESS,nouns[0], nouns[1])

  def findBusNo(self, message):
    tags = self.mecab.pos(message) 
    for i in range(0,len(tags)):
      if tags[i][1] == 'SN' and len(tags) == 1: 
        return BusInfoSearchResult(BusInfoSearchResultCode.SUCCESS,tags[i][0])
      # 810-1
      if tags[i][1] == 'SN' and len(tags) > 2 and tags[i+1][1] == 'SY' and tags[i+2][1] == 'SN':
        return BusInfoSearchResult(BusInfoSearchResultCode.SUCCESS,tags[i][0] + tags[i+1][0] + tags[i+2][0])

      if tags[i][1] == 'SN' and tags[i+1] != 'SN': 
        return BusInfoSearchResult(BusInfoSearchResultCode.SUCCESS,tags[i][0])

      return BusInfoSearchResult(BusInfoSearchResultCode.UNSUPPORTED_FORMAT)
