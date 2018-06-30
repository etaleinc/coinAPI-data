
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '/home/fbuonerba/codes')
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime, timedelta
import time
import calendar
import json
import urllib.request
import multiprocessing as mp

test_key = 'DB318A59-25FF-499E-9A6D-783A19C346D8'

#Free key for testing: test_key = 'EED0F746-36FB-4CC4-8E7C-527333DFA6FB'

api = CoinAPIv1(test_key)

#this function computes how many seconds from now till midnight.
#the correction is due to the fact that some times are not utc by default.
#This can be checked transforming output into utc time.
def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number + 61)# - 14399)



def request_rates(unix_time, base, quote, interval): 
    path='/home/fbuonerba/exchange_rates_data/'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        try:
            exchange=api.exchange_rates_get_specific_rate(base, quote, {'time': utctime})
            with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt', 'w') as outfile:  
                json.dump(exchange, outfile) 
            return(exchange)
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err, unix_time)
                #exceeded daily requests
                time.sleep(until_midnight())
            elif err.code==550 and unix_time>=time.time():
                print(err, unix_time,'too early!')
                #requesting data from the future
                time.sleep(interval)
            else:
                print(err, unix_time, 'unavailable data')
                with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt', 'w') as outfile:  
                    json.dump({}, outfile) 
                #unavailable data. Corresponding file contains only {}
                return None



#unix_time=1530268200
#pool = mp.Pool()#processes=7)
#
#while True:
#    results = [pool.apply_async(request_rates, args=(unix_time - 600*t,'BTC','USD',)) for t in range(8)] 
#    output = [res.get() for res in results]
#    #print(unix_time, output)
#    unix_time+=4800

