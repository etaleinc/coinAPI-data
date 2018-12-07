import csv
import datetime
import time
import os
import multiprocessing as mp
import coinapi_brain as brain
from datetime import datetime

if __name__=='__main__':
    datapath=brain.datapath
    coins=brain.coins
    quotes=brain.quotes
    request_rates=brain.request_rates
    #get beginning of current hour
    T=time.time()
    unix_time=int(T-T%3600)
    utc = datetime.utcfromtimestamp(unix_time).strftime('%Y%m%d')
    #download rates.
    pool=mp.Pool()
    res=[pool.apply_async(request_rates, args=(unix_time,base,quote,)) for base in coins for quote in quotes]
    out=[r.get() for r in res]
    filename=datapath+utc[:4]+'/'+utc[4:6]+'/'+utc[6:]+'/'+utc+'.rates'
    file_exists = os.path.isfile(filename)
    #out contains all rates. Append new rates to existing file.
    with open(datapath+utc[:4]+'/'+utc[4:6]+'/'+utc[6:]+'/'+utc+'.rates', 'a') as outfile:
        name=['time','rate','asset_id_base','asset_id_quote']
        writer=csv.DictWriter(outfile, fieldnames=name)
        if not file_exists:
            writer.writeheader()
        for o in out:
            if o!={}:
                writer.writerow(o)


