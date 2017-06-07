
class PathSearchResultCode(type):
  NONE = 0
  SUCCESS = 201
  NOTFOUND_LOCATION = 401
  NOTFOUND_PATH = 501

class PathSearchResult(object):
  result_code = PathSearchResultCode.NONE
  path = None

  def __init__(self, result_code, path=None):
     self.result_code = result_code
     self.path = path
  

  def getErrorMessage(self):
     if self.result_code == PathSearchResultCode.NOTFOUND_LOCATION:
       return "위치를 찾을 수 없습니다. 정확하게 입력해주세요! "
     elif self.result_code == PathSearchResultCode.NOTFOUND_PATH:
       return "경로를 찾을 수 없습니다. ;("
     return ""

