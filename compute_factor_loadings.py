#compute factor loadings.
#time frame ~ 4 months. First ends April 1st, last ends July 15th.
from mp_functions import compute_factor_loadings as cfl
import json
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import sys
import numpy as np

freq=86400 #frequency for each individual factor

beg=[1515283200+freq*t for t in range(182)]
end=[1522540800+freq*t for t in range(182)]
with open('/home/fbuonerba/codes/meta_data/new_coins.txt') as ff:
    coins=json.load(ff)
bad=['NPXS','MKR','VET','RHOC', 'ONT', 'ZIL', 'NANO', 'BAT','BCD','XTZ']
coins=np.array(coins)
where=[i for i in range(len(coins)) if coins[i] in bad]
coins=np.delete(coins, where)
prettybad=['BCN','DCR','BTG','BTM','XVG']
prettywhere=[i for i in range(len(coins)) if coins[i] in prettybad]
coins=np.delete(coins, prettywhere)
quotes=['BTC']
###################################################
pool=ThreadPool()
##mp process is not allowed to create child processes, but thread does.
##alternative to be checked: create several mp.Process instances, each calling mp.Pool
#pool.daemon=False
results=[pool.apply_async(cfl, args=(coin,quote,beg[t],end[t],freq,)) for coin in coins for quote in quotes for t in range(182)]
pool.close()#avoid memory overload
pool.join()
output = [res.get() for res in results]


#####################################################
# from mp_functions import upload_turnover as ut
# from mp_functions import compute_log_marketcap_exact as clme
# from mp_functions import compute_coin_ratio_exact as ccre

# import multiprocessing as mp
# import json

# freq=604800
# beg=[1515283200+freq*t for t in range(16)]
# end=[1522540800+freq*t for t in range(16)]

# timee=[1515283200+freq*t for t in range(28)]

# with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as ff:
#     coins=json.load(ff)
# quotes=['USD','BTC']

# #for b in coins:
# #    for q in quotes:
# #        for t in range(16):
# #            ut(b,q,beg[t],end[t])

# from mp_functions import compute_returns_variance as crv
# from mp_functions import compute_rates_high_low as crhl
# from mp_functions import compute_returns_strength as crs
# from mp_functions import compute_log_marketcap as clm
# from mp_functions import compute_turnover as ct
# from mp_functions import compute_coin_ratio as ccr


# pool=mp.Pool()
# results=[pool.apply_async(crv, args=(base,quote,b,e,freq,) ) for base in coins for quote in quotes for b in beg for e in end]+[pool.apply_async(crs, args=(base,quote,b,e,freq,) ) for base in coins for quote in quotes for b in beg for e in end]+[pool.apply_async(crhl, args=(base,quote,b,e,freq,) ) for base in coins for quote in quotes for b in beg for e in end]+[pool.apply_async(clm, args=(base,quote,b,e,) ) for base in coins for quote in quotes for b in beg for e in end]+[pool.apply_async(ccr, args=(base,b,e,) ) for base in coins for b in beg for e in end]
# output = [res.get() for res in results]