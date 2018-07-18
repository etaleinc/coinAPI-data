#getting data from CoinMarketCap#
import json
import urllib.request

meta_path='/home/fbuonerba/codes/meta_data/'
with open(meta_path+'cmc_id_list.txt') as filee:
    diction=json.load(filee)

new_path='/home/fbuonerba/cmc_data/'
for i in diction.keys():
    url='https://api.coinmarketcap.com/v2/ticker/'+str(i)+'/'
    web_data= urllib.request.urlopen(url)
    cmc_data=web_data.read()
    cmc=json.loads(cmc_data.decode('utf-8'))
    cmc=cmc['data']
    with open(new_path+'cmc_data_'+cmc['symbol'],'w') as roug:
        json.dump(cmc,roug)
    