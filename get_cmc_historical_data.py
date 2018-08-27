from mp_functions import request_cmc_historical
import datetime
import time

t0=1515283200
#initial time Jan-07
T=time.time()
T-=T%604800
T+=259200
utc_time = datetime.datetime.utcfromtimestamp(T)
date=utc_time.strftime("%Y%m%d")
print(date)
try:
    request_cmc_historical(date)
except Exception as e:
    print(date, e, 'problems')
