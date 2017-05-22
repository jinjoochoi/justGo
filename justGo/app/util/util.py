
def convertToFriendlyTime(min):
  if min >= 60 :
    return str(int(float(min / 60))) + "시간 " + "" if min % 60 is 0 else str(int(float(min % 60))) + "분" 
  else : 
    return str(min) + "분" 
