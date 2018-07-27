#compute factor loadings. Frequency = 1 week for each mean/variance computed.

from mp_functions import compute_returns_variance as crv
from mp_functions import compute_rates_high_low as crhl
from mp_functions import compute_returns_strength as crs
from mp_functions import compute_log_marketcap as clm
from mp_functions import compute_turnover as ct

import multiprocessing as mp
import json

begin=1515283200
end=1522540800
freq=604800

with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as ff:
    coins=json.load(ff)
quotes=['USD','BTC']
for base in coins:
    for quote in quotes:
        ct(base, quote, begin, end)
        

# pool=mp.Pool()
# results=[pool.apply_async(crv, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(crs, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(crhl, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(clm, args=(base,quote,begin,end,) ) for base in coins for quote in quotes]+[pool.apply_async(ct, args=(base,quote,begin,end,) ) for base in coins for quote in quotes]
# output = [res.get() for res in results]