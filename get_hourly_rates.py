import json
import multiprocessing as mp
from mp_functions import request_rates, until_midnight

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'top_coins.txt') as f:
    coins=json.load(f)

unix_time= 1513872000
pool = mp.Pool()
while True:
    results=[pool.apply_async(request_rates, args=(unix_time,coin,'USD',3610,)) for coin in coins]
    output = [res.get() for res in results]
    unix_time+=3600
