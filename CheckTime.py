class CheckTime:
  def isTimeSuspicious(self, time):
    time = int(time)
    if 22 < time <= 24 or time < 5:
      return True
    else: 
      return False