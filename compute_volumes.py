import coinapi_brain as brain
import csv
import time
from datetime import datetime, timedelta

if __name__=='__main__':
    volumes=brain.compute_daily_volumes
    datapath=brain.datapath
    T=time.time()
    unix_time=int(T-T%86400)
    utc = datetime.utcfromtimestamp(unix_time).strftime('%Y%m%d')
    vol=volumes(utc)
    #create file
    names=['time_period_start','time_period_end','asset_id_base','asset_id_quote','volume_traded']
    newfile=datapath+utc[:4]+'/'+utc[4:6]+'/'+utc[6:]+'/'+utc+'.volumes'
    pairs=list(vol.keys())
    with open(newfile, 'w') as outfile:
        writer=csv.DictWriter(outfile, fieldnames=names)
        writer.writeheader()
        for c in pairs:
            writer.writerow(vol[c])
    