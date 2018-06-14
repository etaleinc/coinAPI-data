
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime
import time
from time import mktime as mktime
import calendar
import json

test_key = 'EED0F746-36FB-4CC4-8E7C-527333DFA6FB'

api = CoinAPIv1(test_key)

symbols = api.metadata_list_symbols()


# In[20]:


#This function downloads data in json format.
#For a time and symbol, we get one unit of data with one request.
def download_data(unix_time, symbol):
    #Convert unix_time in utc with format '%Y-%m-%dT%H:%M:%S'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    trades_historical_data=api.trades_historical_data(symbol['symbol_id'],{'time_start': utctime , 'limit':1})
    
    with open('trades_historical_data_'+str(unix_time)+'.txt', 'w') as outfile:  
        json.dump(trades_historical_data, outfile)


# In[ ]:


#This function iterates the json download above. 
def download_json_simple_loop(unix_time):
    sym=symbols[7]
    for i in range(2):
        download_data(unix_time + 60*i, sym)
    


# In[22]:


#This function creates a pandas dataframe out of the file downloaded above.
def make_dataframe(unix_time, symbol):
    
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    
    with open('trades_historical_data_'+str(unix_time)+'.txt') as json_file:  
        trades_historical_data = json.load(json_file)
    
    
    if trades_historical_data==[]:
        df=pd.DataFrame()
    else:   
        df=pd.DataFrame(data=trades_historical_data)
        #drop and add new columns.
        df=df.drop(['time_coinapi'], axis=1)
        df=df.drop(['symbol_id'], axis=1)
        df['unix_time']=unix_time
        df['human_time']=utctime
        df['asset_base']=symbol['asset_id_base']
        df['asset_quote']=symbol['asset_id_quote']
        df['exchange_id']=symbol['exchange_id']
        df['type']=symbol['symbol_type']
#       Coherence=[]
#       if df['ask_price'][0]>df['bid_price'][0]: 
#           Coherence.append('')
#       else:
#           Coherence.append('X')
        df['actual_time_exchange']=df['time_exchange']
        df=df.drop(['time_exchange'],axis=1)
#        df['crossed_market']=Coherence
#        #move columns around.
        col=df.columns
        col1=col[4:6].append(col[0:4]).append(col[6:])
        df=df[col1]
    
    return(df)


# In[23]:


def simple_loop(unix_time):
    sym=symbols[7]
    df = pd.DataFrame()
    for i in range(2):
        df = pd.concat([df, make_dataframe(unix_time+60*i, sym)])
    return(df)    


# In[24]:


#This function creates a csv file out of the dataframe created above
def make_csv(unix_time):
    df=simple_loop(unix_time)
    df.to_csv('trades_test.csv', index=False)
    


# In[26]:


#This is how to implement the data collection.
unix_time= 1451606400
download_json_simple_loop(unix_time)
make_csv(unix_time)

