from mp_functions import request_cmc_historical
import datetime
import time

t0=1515283200
#initial time Jan-07
T=time.time()
utc_time = datetime.datetime.utcfromtimestamp(T)
date=utc_time.strftime("%Y%m%d")
try:
    request_cmc_historical(date)
except Exception as e:
    print(date, e, 'problems')
