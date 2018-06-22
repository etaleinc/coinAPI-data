
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

def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number - 14399)

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
        utctime = datetime.utcfromtimestamp(self.unix_time).strftime('%Y-%m-%dT%H:%M:%S')
        while True:
            try:
                exchange=api.exchange_rates_get_specific_rate(self.base, self.quote, {'time': utctime})
                with self.output().open('w') as outfile:
                    json.dump(exchange, outfile) 
                break
            except urllib.error.HTTPError as err:
                print(err.code)
                time.sleep(until_midnight())       

#download data with request_exchange_rates sampled every 10 minutes=600 seconds.
#every iteration consists of 1000 parallel requests.
beginning=1505384400
while True:
    luigi.build([request_exchange_rates(unix_time=beginning+600*t, base='BTC', quote='USD') for t in range(1000)], workers=1000, local_scheduler=True)
    beginning+=600000

