import json
import multiprocessing as mp
from mp_functions import request_rates, until_midnight

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'new_coins.txt') as f:
    coins=json.load(f)
    
quotes=['USD','BTC']
unix_time=1514764800
pool = mp.Pool()


while True:
    results=[pool.apply_async(request_rates, args=(unix_time,coin,quote,)) for coin in coins for quote in quotes]
    output = [res.get() for res in results]
    unix_time+=3600

