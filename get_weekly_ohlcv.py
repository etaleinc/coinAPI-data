import time
import json
import multiprocessing as mp
from mp_functions import upload_ohlcv_weekly as uow

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'new_symbols.txt') as f:
    symbols=json.load(f)
unix_time=1515283200
pool = mp.Pool()
results=[pool.apply_async(uow, args=(unix_time,symbol,)) for symbol in symbols]
output = [res.get() for res in results]

