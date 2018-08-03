#compute factor loadings. Frequency = 1 week.
#time frame ~ 4 months. First ends April 1st, last ends July 15th.
from mp_functions import upload_turnover as ut
import multiprocessing as mp
import json

freq=604800
beg=[1515283200+freq*t for t in range(16)]
end=[1522540800+freq*t for t in range(16)]

with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as ff:
    coins=json.load(ff)
quotes=['USD','BTC']
pool=mp.Pool()
results=[pool.apply_async(ut(b,q,beg[t],end[t],)) for b in coins for q in quotes for t in range(16)]
output=[res.get() for res in results]
# from mp_functions import compute_returns_variance as crv
# from mp_functions import compute_rates_high_low as crhl
# from mp_functions import compute_returns_strength as crs
# from mp_functions import compute_log_marketcap as clm
# from mp_functions import compute_turnover as ct
# from mp_functions import compute_coin_ratio as ccr

# import multiprocessing as mp
# import json

# begin=1517702400
# end=1525564800
# freq=604800

# with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as ff:
#     coins=json.load(ff)
# quotes=['USD','BTC']
# for base in coins:
#     for quote in quotes:
#         ct(base, quote, begin, end)
        

# pool=mp.Pool()
# results=[pool.apply_async(crv, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(crs, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(crhl, args=(base,quote,begin,end,freq,) ) for base in coins for quote in quotes]+[pool.apply_async(clm, args=(base,quote,begin,end,) ) for base in coins for quote in quotes]+[pool.apply_async(ccr, args=(base,begin,end,) ) for base in coins]
# output = [res.get() for res in results]