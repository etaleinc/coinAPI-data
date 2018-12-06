import csv
import datetime
import time
import multiprocessing as mp
import coinapi_brain as brain
from datetime import datetime     

if __name__=='__main__':
    request_ohlcv=brain.request_ohlcv
    datapath=brain.datapath
    coins=brain.coins
    quotes=brain.quotes
    symbols=brain.symbols
    #get beginning of current day
    T=time.time()
    unix_time=int(T-T%86400)
    utc = datetime.utcfromtimestamp(unix_time).strftime('%Y%m%d')
    #download ohlcv: for each symbol get ohlcv data.
    pool=mp.Pool()
    res=[[sym , pool.apply_async(request_ohlcv, args=(unix_time,sym,))] for sym in symbols]
    out=[[r[0],r[1].get()] for r in res]
    #out contains all rates. Create file.
    with open(datapath+utc[:4]+'/'+utc[4:6]+'/'+utc[6:]+'/'+utc+'.ohlcv', 'w') as outfile:
        name=['time_close','time_open','price_close','price_open', 'asset_id_base','asset_id_quote','exchange','trades_count','volume_traded', 'price_high', 'price_low','time_period_start','time_period_end'] 
        writer=csv.DictWriter(outfile, fieldnames=name)
        writer.writeheader()
        for o in out:
            if o[1]!=[]:
                row=o[1][0]
                sym=o[0].split('_')
                base, quote, exchange=sym[2],sym[3],sym[0]
                if base=='SPOT':
                    base=sym[3]
                    quote=sym[1]
                row['asset_id_base']=base
                row['asset_id_quote']=quote
                row['exchange']=exchange
                writer.writerow(row)



