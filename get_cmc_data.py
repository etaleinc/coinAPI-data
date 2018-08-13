#getting data from CoinMarketCap#
import json
import urllib.request
from datetime import datetime, time
import requests

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'cmc_id_list.txt') as filee:
    diction=json.load(filee)
headers = {'Accept': 'text/html'}
midnight = datetime.combine(datetime.today(), time.min)
unix_midnight=midnight.strftime('%s')


new_path='/home/fbuonerba/cmc_data/'
for i in diction.keys():
    url='https://api.coinmarketcap.com/v2/ticker/'+str(i)+'/'
    web_data= requests.get(url, headers=headers)
    cmc_data=web_data.content
    cmc=json.loads(cmc_data.decode('utf-8'))
    cmc=cmc['data']
    if cmc is not None:
        if cmc['symbol']=='MIOTA':
            diction[i]='IOTA'
    with open(new_path+'cmc_'+diction[i]+'_'+str(unix_midnight)+'.txt','w') as roug:
        json.dump(cmc,roug)
    
