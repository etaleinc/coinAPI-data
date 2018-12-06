import datetime
import time
import requests
import json
import csv
import coinapi_brain as brain

if __name__ == "__main__":
    datapath=brain.datapath
    request_cmc_historical=brain.request_cmc_historical
    t0=1515283200
    #initial time Jan-07
    T=time.time()
    T=T-T%604800
    #get data from previous sunday
    T+=259200
    T-=604800
    utc_time = datetime.datetime.utcfromtimestamp(T)
    date=utc_time.strftime("%Y%m%d")
    historical=request_cmc_historical(date)
    path=datapath+date[:4]+'/'+date[4:6]+'/'+date[6:]+'/'
    fieldname=['symbol','supply','price', 'volume']
    with open(path+date+'.cmc_historical','w') as outfile:
        writer=csv.DictWriter(outfile, fieldnames=fieldname)
        writer.writeheader()
        for c in list(historical.keys()):
            writer.writerow(historical[c])
  