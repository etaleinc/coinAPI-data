
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime, timedelta
import time
from time import mktime as mktime
import calendar
import json
import urllib.request


test_key = 'DB318A59-25FF-499E-9A6D-783A19C346D8'

api = CoinAPIv1(test_key)


# In[2]:


#this function computes how many seconds from now till midnight.
#the correction is due to the fact that some times are not utc by default.
#This can be checked transforming output into utc time.
def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number - 14399)


# In[3]:


#Check whether list of assets is already available.
#If not, download it.
def get_assets():
    try:
        with open('assets.txt') as json_file:  
            assets= json.load(json_file)
    except:
        assets = api.metadata_list_assets()
        with open('assets.txt', 'w') as outfile:  
            json.dump(assets, outfile)  
    return(assets)


# In[4]:


#Check whether list of symbols is already available.
#If not, download it.
def get_symbols():
    try:
        with open('symbols.txt') as json_file:  
            symbols = json.load(json_file)
    except:
        symbols = api.metadata_list_symbols()
        with open('symbols.txt', 'w') as outfile:  
            json.dump(symbols, outfile)  
    return(symbols)


# In[1]:


#this function sends a request to the coinAPI server.
#If it goes through, it creates a json file with data in 
#path directory.
#If an error returns, it pauses for 60 seconds and prints error.
def request_exchange_rates(unix_time, base, quote):
    path='/home/fbuonerba/exchange_rates_data/'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        try:
            exchange=api.exchange_rates_get_specific_rate(base, quote, {'time': utctime})
            with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt', 'w') as outfile:  
                json.dump(exchange, outfile) 
            break
        
        except urllib.error.HTTPError as err:
            print(err.code)
            time.sleep(60)
    return(exchange)


# In[6]:


#This function calls data from json files in path directory.
#If such data is not available, download it using the previous request function.
def upload_exchange_rates(unix_time, base, quote):
    path='/home/fbuonerba/exchange_rates_data/'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    try:
        with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt') as json_file:  
            exchange = json.load(json_file)   
    except:
        #print('downloading...')
        exchange=request_exchange_rates(unix_time, base, quote)   
    return(exchange)  


# In[7]:


#this function sends a request to the coinAPI server.
#If it goes through, it creates a json file with data in 
#path directory.
#If an error returns, it pauses until midnight to send 
#one more request (daily limit is hit).
def request_trades(unix_time, symbol):
    #path='Users/federicobuonerba/Documents/Etale/etale_data/trades_data/'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        try:
            trades_historical_data=api.trades_historical_data(symbol['symbol_id'],{'time_start': utctime , 'limit':1})
            with open('trades_historical_data_'+str(unix_time)+'.txt', 'w') as outfile:  
                json.dump(trades_historical_data, outfile)
            break
        except urllib.error.HTTPError:
            time.sleep(until_midnight())
    return(trades_historical_data)


# In[9]:


#This function calls data from json files in path directory.
#If such data is not available, download it using the previous request function.

def upload_trades(unix_time, symbol):
    
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    #path='Users/federicobuonerba/Documents/Etale/etale_data/trades_data/'
    try:
        with open('trades_historical_data_'+str(unix_time)+'.txt', 'r') as json_file:  
            trades_historical_data = json.load(json_file)   
    except:
        #print('downloading...')
        trades_historical_data=request_trades(unix_time, symbol)
    return(trades_historical_data)  


# In[4]:


def make_trades_df(unix_time, symbol):
    
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    trades_historical_data = upload_trades(unix_time, symbol)
    if trades_historical_data==[]:
        df=pd.DataFrame()
    else:   
        df=pd.DataFrame(data=trades_historical_data)
        df=df.drop(['time_coinapi'], axis=1)
        df=df.drop(['symbol_id'], axis=1)
        df['unix_time']=unix_time
        df['human_time']=utctime
        df['asset_base']=symbol['asset_id_base']
        df['asset_quote']=symbol['asset_id_quote']
        df['exchange_id']=symbol['exchange_id']
        df['type']=symbol['symbol_type']
        df['actual_time_exchange']=df['time_exchange']
        df=df.drop(['time_exchange'],axis=1)
        col=df.columns
        col1=col[4:6].append(col[0:4]).append(col[6:])
        df=df[col1]
    
    return(df)


# In[ ]:


def make_quotes_df(unix_time, symbol):
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    ####Make request and get functions for quotes as well, instead of calling api.
    #####################################################
    quotes_historical_data=api.quotes_historical_data(symbol['symbol_id'],{'time_start': utctime , 'limit':1})
    if quotes_historical_data==[]:
        df=pd.DataFrame()
    else:    
    
        df=pd.DataFrame(data=quotes_historical_data)
        #drop and add new columns.
        df=df.drop(['time_coinapi'], axis=1)
        df=df.drop(['symbol_id'], axis=1)
        df['unix_time']=unix_time
        df['human_time']=utctime
        df['asset_base']=symbol['asset_id_base']
        df['asset_quote']=symbol['asset_id_quote']
        df['exchange_id']=symbol['exchange_id']
        df['type']=symbol['symbol_type']
        Coherence=[]
        if df['ask_price'][0]>df['bid_price'][0]: 
            Coherence.append('')
        else:
            Coherence.append('X')
        df['actual_time_exchange']=df['time_exchange']
        df=df.drop(['time_exchange'],axis=1)
        df['crossed_market']=Coherence
        #move columns around.
        col=df.columns
        col1=col[4:6].append(col[0:4]).append(col[6:])
        df=df[col1]
    
    return(df)

def make_ohlcv_df(unix_time, symbol):
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    ####Make request and get functions for quotes as well, instead of calling api.
    #####################################################
    ohlcv_historical=api.ohlcv_historical_data(symbol['symbol_id'], {'period_id': '1MIN', 'time_start': utctime, 'limit': 1})
    if ohlcv_historical==[]:
        df=pd.DataFrame()
    else:    
    
        df=pd.DataFrame(data=ohlcv_historical)
        #drop and add new columns.
        df=df.drop(['time_period_start'], axis=1)
        df=df.drop(['time_period_end'], axis=1)
        df=df.drop(['time_open'], axis=1)
        df=df.drop(['time_close'], axis=1)
        df['unix_time_start']=unix_time
        df['human_time_start']=utctime
        df['asset_base']=symbol['asset_id_base']
        df['asset_quote']=symbol['asset_id_quote']
        df['exchange_id']=symbol['exchange_id']
        df['type']=symbol['symbol_type']
        col=df.columns
        col1=col[6:8].append(col[0:6]).append(col[8:])
        df=df[col1]
    
    return(df)
#####Below: sample loop functions. They need to be improved.######

#this function loops make_df over all possible symbols
def get_data_symbols(unix_time):
    df = pd.DataFrame()
    for symbol in symbols:
        df_new=make_df(unix_time, symbol)
        df=pd.concat([df, df_new])
    return(df)


# In[ ]:


#this function loops get_data_symbols for the day starting at unix_time,
#sampled every hour. There are 1440 minutes in a day.
def get_hourly_data_day(unix_time, interval):
    df=pd.DataFrame()
    for t in range(24):
        df_new=get_data_symbols(unix_time + 3600*t)
        df=pd.concat([df, df_new])
    return(df)    
        


# In[7]:


#this function loops get_data_symbols for the day starting at unix_time,
#sampled every minute. There are 1440 minutes in a day.
def get_minutely_data_day(unix_time, interval):
    df=pd.DataFrame()
    for t in range(1440):
        df_new=get_data_symbols(unix_time + 60*t)
        df=pd.concat([df, df_new])
    return(df)    
        
    


# In[31]:


#this function creates a csv of the daily dataframe constructed with get_data_time
def create_csv(unix_time):
    df=get_daily_data(unix_time)
    df.to_csv('trades_historical_data_'+str(unix_time)+'.csv', index=False)

