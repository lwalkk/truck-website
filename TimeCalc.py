
from datetime import datetime, timedelta
from dateutil import rrule
import numpy as np

elapsedTime = []
wait_times = [] 

def CalculateWaitTime(times, onSite):
  for row in times:
      elapsedTime.append((datetime.strptime(str(row['time_out']),'%Y-%m-%d %H:%M:%S') 
      - datetime.strptime(str(row['time_in']),'%Y-%m-%d %H:%M:%S')))

  avgTime = np.mean(elapsedTime)
  
  for row in onSite:
    wait_times.append(row['time_in'] + avgTime)
  
  return wait_times

