
# coding: utf-8

# In[1]:


import luigi
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '/home/fbuonerba')
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime, timedelta
import time
import calendar
import json
import urllib.request


test_key = 'DB318A59-25FF-499E-9A6D-783A19C346D8'

api = CoinAPIv1(test_key)


# In[2]:


def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    almost=(midnight - datetime.now()).seconds
    #returns midnight + 1 minute in utc.
    return (almost + 61)


# In[3]:


class request_exchange_rates(luigi.Task):
    unix_time=luigi.Parameter()
    base=luigi.Parameter()
    quote=luigi.Parameter()
    path='/home/fbuonerba/exchange_rates_data/'
    
    def requires(self):
        return None
    def output(self):
        return luigi.LocalTarget(self.path+'exchange_rate_'+str(self.base)+'_'+str(self.quote)+'_'+str(self.unix_time)+'.txt')
    
    def run(self):
        
        while True:
            try:
                utctime = datetime.utcfromtimestamp(self.unix_time).strftime('%Y-%m-%dT%H:%M:%S')
                exchange=api.exchange_rates_get_specific_rate(self.base, self.quote, {'time':utctime})
                with self.output().open('w') as outfile:
                    json.dump(exchange, outfile) 
                break
            except urllib.error.HTTPError as err:
                print(err)
                wake_up=until_midnight()
                time.sleep( wake_up )          
                
#cpu=8, should use that many parallel processes.                
beginning=1529861400
while True:
    luigi.build([request_exchange_rates(unix_time=beginning+600*t, base='BTC', quote='USD') for t in range(8)], local_scheduler=True, workers=8)       
    beginning+=4800
