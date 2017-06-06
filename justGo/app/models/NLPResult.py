
class NLPResultCode(type):
  NONE = 0
  SUCCESS = 201
  UNSUPPORTED_FORMAT = 33301

class NLPResult(object):
  result_code = NLPResultCode.NONE
  src, dest = None, None

  def __init__(self, result_code, src=None, dest=None):
     self.result_code = result_code
     self.src = src
     self.dest = dest

  def getErrorMessage(self):
     if self.result_code == NLPResultCode.UNSUPPORTED_FORMAT:
       return "장소를 인식하지 못했어요. 조금 더 정확하게 입력해주세요! :)"

