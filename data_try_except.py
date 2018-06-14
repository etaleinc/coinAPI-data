
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '/home/fbuonerba')
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime
import time
from time import mktime as mktime
import calendar
import json

test_key = 'EED0F746-36FB-4CC4-8E7C-527333DFA6FB'

api = CoinAPIv1(test_key)


# In[2]:


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


# In[3]:


#This function checks whether certain data has already been downloaded.
#If not, it downloads it.
def get_data(unix_time, symbol):
    
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    try:
        with open('trades_historical_data_'+str(unix_time)+'.txt') as json_file:  
            trades_historical_data = json.load(json_file)   
    except:
        #print('downloading...')
        trades_historical_data=api.trades_historical_data(symbol['symbol_id'],{'time_start': utctime , 'limit':1})
        with open('trades_historical_data_'+str(unix_time)+'.txt', 'w') as outfile:  
            json.dump(trades_historical_data, outfile)    
    return(trades_historical_data)  


# In[4]:


def make_df(unix_time, symbol):
    
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    trades_historical_data = get_data(unix_time, symbol)
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


# In[6]:


#Example
symbols=get_symbols()
unix_time= 1451606400
make_df(unix_time, symbols[8])


# In[14]:


#this function loops make_df over all possible symbols
def get_data_symbols(unix_time):
    df = pd.DataFrame()
    for symbol in symbols:
        df_new=make_df(unix_time, symbol)
        df=pd.concat([df, df_new])
    return(df)


# In[31]:


#this function loops get_data_symbols for the day starting at unix_time,
#sampled every minute. There are 1440 minutes in a day.
def get_daily_data(unix_time):
    df=pd.DataFrame()
    for t in range(1440):
        df_new=get_data_symbols(unix_time + 60*t)
        df=pd.concat([df, df_new])
    return(df)    
        
    


# In[32]:


#this function creates a csv of the daily dataframe constructed with get_data_time
def create_csv(unix_time):
    df=get_daily_data(unix_time)
    df.to_csv('trades_historical_data_'+str(unix_time)+'.csv', index=False)

