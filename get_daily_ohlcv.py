import time
import json
import multiprocessing as mp
from mp_functions import request_ohlcv, until_midnight, previous_midnight

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'top_coins.txt') as f:
    coins=json.load(f)
quotes=['USD','BTC']
with open(meta_path+'top_exchanges.txt') as ff:
    exchanges=json.load(ff)
unix_time=1522540800
pool = mp.Pool()
while True:
    results=[pool.apply_async(request_ohlcv, args=(unix_time,coin,quote, exchange, 1,)) for coin in coins for quote in quotes for exchange in exchanges]
    output = [res.get() for res in results]
    unix_time += 86400

