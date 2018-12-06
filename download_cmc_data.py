#getting data from CoinMarketCap#
import coinapi_brain as brain
import urllib.request
import json
import requests
import csv
from datetime import datetime, time

diction=brain.cmc_index
datapath=brain.datapath
headers = {'Accept': 'text/html'}

midnight = datetime.combine(datetime.today(), time.min)
t=str(midnight)[:10].split('-')[:3]

with open(datapath+t[0]+'/'+t[1]+'/'+t[2]+'/'+t[0]+t[1]+t[2]+'.cmc_daily','w') as outfile:
    writer=csv.DictWriter(outfile, fieldnames=['rank','website_slug','max_supply','id','name','circulating_supply','total_supply','symbol','last_updated','quotes'])
    for i in diction.keys():
        url='https://api.coinmarketcap.com/v2/ticker/'+str(i)+'/'
        web_data= requests.get(url, headers=headers)
        cmc_data=web_data.content
        cmc=json.loads(cmc_data.decode('utf-8'))
        cmc=cmc['data']
        if cmc is not None:
            if cmc['symbol']=='MIOTA':
                diction[i]='IOTA'
        try:
            writer.writerow(cmc)
        except Exception as e:
            print(e)

   