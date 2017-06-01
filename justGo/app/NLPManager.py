from konlpy.tag import Mecab

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
    return nouns[0], nouns[1]
