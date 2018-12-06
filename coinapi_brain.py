import numpy as np
import sys
import time
import calendar
import json
import urllib.request
import requests
import csv
import multiprocessing as mp
from bs4 import BeautifulSoup
from coinapi_v1 import CoinAPIv1
from datetime import datetime, timedelta, date

test_key = 'DB318A59-25FF-499E-9A6D-783A19C346D8'
#Free key for testing: test_key = 'EED0F746-36FB-4CC4-8E7C-527333DFA6FB'
api = CoinAPIv1(test_key)
quotes=['USD','BTC']
datapath='/home/databot/data/coinapi/'
metapath='/home/fbuonerba/codes/meta_data/'
with open(metapath+'new_coins.txt') as f:
    coins=json.load(f)
with open(metapath+'new_symbols.txt') as symfile:
    symbols=json.load(symfile)
with open(metapath+'new_cmc_id.txt') as filee:
    cmc_index=json.load(filee)

def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number + 61)# - 14399)

def request_rates(unix_time, base, quote):
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        #check if it's too early for such request:
        if unix_time >= time.time():
            print('rates, wait ', unix_time-time.time(), 'seconds.')
            time.sleep(unix_time-time.time()+5)
        try:
            exchange=api.exchange_rates_get_specific_rate(base, quote, {'time': utctime})
            return(exchange)
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err.code, utctime)
                time.sleep(until_midnight())
            elif err.code==401:
                print(err.code, utctime)
                #invalid api key
                break
            else:
                #unavailable data. Corresponding file contains only {}
                return( {} )
            
def request_ohlcv(unix_time, sym_id):
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        #check if it's too early for such request:
        if unix_time >= time.time():
            print('ohlcv, wait ', unix_time-time.time(), 'seconds.')
            time.sleep(unix_time-time.time()+5)
        #if it's not too early, try and send a request.
        try:
            ohlcv=api.ohlcv_historical_data(sym_id, {'period_id': '1DAY', 'time_start':utctime, 'limit': 1})
            return(ohlcv)
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err.code, utctime)
                #exceeded daily requests
                time.sleep(until_midnight())
            elif err.code==401:
                print(err.code, utctime)
                #invalid api key
                break
            else:
                #unavailable data
                return( [] )    
            
            
def request_cmc_historical(date):
    #date=YYYYMMDD
    headers = {'Accept': 'text/html'}
    url='https://coinmarketcap.com/historical/'+str(date)+'/'
    web_data= requests.get(url, headers=headers)
    cmc_data=web_data.content
    soup=BeautifulSoup(cmc_data, 'html.parser')
    #scrape volumes
    Vol=[]
    SoVolume=soup.find_all(class_='volume')
    for x in SoVolume:
        x=x.contents[0].replace('$','').replace(',','')
        x=x.replace('Low Vol','0')
        x=int(float(x))
        Vol.append(x)
    #scrape supplies. This is tricky since for some reasons tag change over time.
    #sometimes it is <a data-supply... sometimes it is <span data-supply...
    So=soup.find_all('td')
    Supply=[]
    for x in So:
        if x.contents[0]=='\n':
            z=str(x.contents[1])
            if 'data-supply' in z:
                y=z.split('=')[1].split('data')[0].split('"')[1]
                if y=='None':
                    y=float('nan')
                else:
                    y=float(y)
                Supply.append(y)
    #scrape prices
    Price=[]
    SoPrice=soup.find_all(class_='price')
    for x in SoPrice:
        x=x.contents[0].replace('$','').replace(',','')
        x=float(x)
        Price.append(x)
    #scrape coins symbols
    Syms=[]
    SoSym=soup.find_all(class_="text-left col-symbol")
    for x in SoSym:
        x=str(x.contents[0])
        Syms.append(x)
    #make a dictionary with all data    
    data={}
    for i in range(len(Supply)):
        data[Syms[i]]={'symbol': Syms[i],'volume': Vol[i], 'price': Price[i], 'supply': Supply[i]}
    #reduce the dictionary to include only new_coins.
    #Possible errors if new_coins do not appear in data.keys()
    finaldictio={}
    for c in cmc_index.values():
        try:
            finaldictio[c]=data[c]
        except:
            finaldictio[c]={'symbol':c,'volume': float('nan'), 'price': float('nan'), 'supply': float('nan')}
    return(finaldictio)


def compute_daily_volumes(date):
    #YYYYMMDD
    volume={}
    file=datapath+date[:4]+'/'+date[4:6]+'/'+date[6:]+'/'+date+'.ohlcv'
    with open(file, 'r') as infile:
        ohlcv=csv.DictReader(infile)
        for row in ohlcv:
            rowsym=row['asset_id_base']+'_'+row['asset_id_quote']
            if rowsym not in volume.keys():
                volume[rowsym]={}
                volume[rowsym]['time_period_start']=row['time_period_start']
                volume[rowsym]['time_period_end']=row['time_period_end']
                volume[rowsym]['asset_id_base']=row['asset_id_base']
                volume[rowsym]['asset_id_quote']=row['asset_id_quote']
                volume[rowsym]['volume_traded']=0
            volume[rowsym]['volume_traded']+=float(row['volume_traded'])
    return(volume)

