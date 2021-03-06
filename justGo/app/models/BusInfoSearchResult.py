
class BusInfoSearchResultCode(type):
  NONE = 0
  SUCCESS = 201
  UNSUPPORTED_FORMAT = 301
  NOTFOUND = 401

class BusInfoSearchResult(object):
  result_code = BusInfoSearchResultCode.NONE
  bus_info = None
 
  def __init__ (self, result_code, bus_info=None):
    self.result_code = result_code
    self.bus_info = bus_info

  def getErrorMessage(self):
    if self.result_code == BusInfoSearchResultCode.NOTFOUND:
      return "해당 버스에 대한 정보를 찾을 수 없네요. ;(  다시 한번 확인해주세요!"
    if self.result_code == BusInfoSearchResultCode.UNSUPPORTED_FORMAT:
      return "버스 번호를 정확하게 입력하셨나요? ;(  다시 한번 확인해주세요!"
