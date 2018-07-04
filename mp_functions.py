#####Functions for data collection. 
#####Requests are designed to submit requests to coinAPI and handle errors.
#####Uploads are designed to upload the data in the work pipeline.
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

def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number + 61)# - 14399)

def previous_midnight():
    ye = datetime.now() - timedelta(1)
    ye_midnight = datetime(year=ye.year, month=ye.month, day=ye.day, hour=0, minute=0, second=0)
    right_number=(ye_midnight).timestamp()
    return(right_number - 61)

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
                #time.sleep(until_midnight())
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

def request_ohlcv(unix_time, base, quote, exchange, interval, limit):
    path='/home/fbuonerba/ohlcv_data/ohlcv_'
    sym_id=str(exchange)+'_SPOT_'+str(base)+'_'+str(quote)
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        try:
            ohlcv=api.ohlcv_historical_data(sym_id, {'period_id': '1DAY', 'time_start':utctime, 'limit': limit})
            for j in range(len(ohlcv)):
                with open(path+sym_id+'_'+str(unix_time+j*86400)+'_'+str(unix_time+(j+1)*86400)+'.txt', 'w') as ff:
                    json.dump(ohlcv[j],ff)
            return ohlcv
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
                for j in range(limit):
                    with open(path+sym_id+'_'+str(unix_time+j*86400)+'_'+str(unix_time+(j+1)*86400)+'.txt', 'w') as ff:
                        json.dump({},ff)
                #unavailable data
                ohlcv=[]
                return ohlcv          
            


            
def upload_rates(unix_time, base, quote):
    path='/home/fbuonerba/exchange_rates_data/'
    try:
        with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt') as json_file:
            exchange = json.load(json_file)    
    except:
        exchange=request_rates(unix_time, base, quote, 0) 
    return(exchange)
    

def upload_ohlcv(unix_time, base quote, exchange, limit):
    path='/home/fbuonerba/ohlcv_data/'
    sym_id=str(exchange)+'_SPOT_'+str(base)+'_'+str(quote)
    try:
        with open(path+sym_id+'_'+str(unix_time)+'_'+str(unix_time+86400)+'.txt') as json_file:
            ohlcv = json.load(json_file)    
    except:
        ohlcv=request_ohlcv(unix_time, base, quote, exchange, 0, 1) 
    return(ohlcv)
    
def compute_log_return(unix_time, base, quote, interval):
    path1='/home/fbuonerba/exchange_rates_data/'
    with open(path1+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt') as file1:
        ret1=json.load(file1)
    with open(path1+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time+interval)+'.txt') as file2:
        ret2=json.load(file2)
    log_ret=np.log(ret2['rate'])-np.log(ret1['rate'])
    path2='/home/fbuonerba/log_returns_data/'
          name=path2+'log_return_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'_'+str(unix_time+interval)+'.txt'
    with open(name,'w') as ff:
        json.dump(log_ret,ff)
    return(log_ret)