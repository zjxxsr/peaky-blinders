import datetime
import time

dt1 = datetime.datetime.now()
time.sleep(1.5)
dt2 = datetime.datetime.now()
duration = dt2 - dt1
print(duration.total_seconds())
