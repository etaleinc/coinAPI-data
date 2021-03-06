#####Functions for data collection. 
#####Requests are designed to submit requests to coinAPI and handle errors.
#####Uploads are designed to upload the data in the work pipeline.
import numpy as np
import sys
sys.path.insert(0, '/home/fbuonerba/codes')
from coinapi_v1 import CoinAPIv1
import datetime
from datetime import datetime, timedelta
import time
import calendar
import json
import urllib.request
import requests
import multiprocessing as mp
from bs4 import BeautifulSoup

test_key = 'DB318A59-25FF-499E-9A6D-783A19C346D8'

#Free key for testing: test_key = 'EED0F746-36FB-4CC4-8E7C-527333DFA6FB'

api = CoinAPIv1(test_key)

def until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    wrong_number=(midnight - datetime.now()).seconds
    return (wrong_number + 61)# - 14399)

def previous_midnight():
    ye = datetime.now() - timedelta(1)
    ye_midnight = datetime(year=ye.year, month=ye.month, day=ye.day, hour=0, minute=0, second=0)
    right_number=(ye_midnight).timestamp()
    return(right_number - 61)

def request_rates(unix_time, base, quote): 
    path='/home/fbuonerba/exchange_rates_data/'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        #check if it's too early for such request:
        if unix_time+10>=time.time():
            print('rates, wait ', unix_time-time.time()+10, 'seconds;', 'unix_time=',unix_time, base, quote)
            time.sleep(unix_time-time.time()+10)
        try:
            exchange=api.exchange_rates_get_specific_rate(base, quote, {'time': utctime})
            with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt', 'w') as outfile:  
                json.dump(exchange, outfile) 
            return(exchange)
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err.code, unix_time)
                #exceeded daily requests
                time.sleep(until_midnight())
            elif err.code==401:
                print(err.code, unix_time)
                #invalid api key
                break
            else:
                with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt', 'w') as outfile:  
                    json.dump({}, outfile) 
                #unavailable data. Corresponding file contains only {}
                return( {} )

def request_ohlcv(unix_time, sym_id, limit):
    path='/home/fbuonerba/ohlcv_data/ohlcv_'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        #check if it's too early for such request:
        if unix_time + limit*86400 +10>=time.time():
            #number of days after unix_time:
            time_ahead=time.time()+until_midnight()-unix_time
            print('ohlcv, starting midnight wait for', limit-int(time_ahead/86400), 'days;', unix_time, sym_id)
            time.sleep(until_midnight()+86400*limit-time_ahead +10)
        #if it's not too early, try and send a request.
        try:
            ohlcv=api.ohlcv_historical_data(sym_id, {'period_id': '1DAY', 'time_start':utctime, 'limit': limit})
            for j in range(len(ohlcv)):
                with open(path+sym_id+'_'+str(unix_time+j*86400)+'_'+str(unix_time+(j+1)*86400)+'.txt', 'w') as ff:
                    json.dump(ohlcv[j],ff)
            return ohlcv
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err.code, unix_time)
                #exceeded daily requests
                time.sleep(until_midnight())
            elif err.code==401:
                print(err.code, unix_time)
                #invalid api key
                break
            else:
                #print(err, unix_time, 'unavailable data')
                for j in range(limit):
                    with open(path+sym_id+'_'+str(unix_time+j*86400)+'_'+str(unix_time+(j+1)*86400)+'.txt', 'w') as ff:
                        json.dump([],ff)
                #unavailable data
                return( [] )     
            

def request_ohlcv_weekly(unix_time, sym_id):
    path='/home/fbuonerba/ohlcv_data/ohlcv_'
    utctime = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
    while True:
        #check if it's too early for such request:
        now=time.time()
        if unix_time + 604800>=now:
            print('weekly ohlcv', unix_time, sym_id, 'wait for: seconds', unix_time+604805-now)
            time.sleep(unix_time+604805-now)
        #if it's not too early, try and send a request.
        try:
            ohlcv=api.ohlcv_historical_data(sym_id, {'period_id': '7DAY', 'time_start':utctime})
            if len(ohlcv)>0:
                for j in range(len(ohlcv)):
                    with open(path+sym_id+'_'+str(unix_time+j*604800)+'_'+str(unix_time+(j+1)*604800)+'.txt', 'w') as ff:
                        json.dump(ohlcv[j],ff)
                return ohlcv[0]
            else:
                for j in range(len(ohlcv)):
                    with open(path+sym_id+'_'+str(unix_time+j*604800)+'_'+str(unix_time+(j+1)*604800)+'.txt', 'w') as ff:
                        json.dump([],ff)
                return ohlcv
        except urllib.error.HTTPError as err:
            if err.code==429:
                print(err.code, unix_time)
                #exceeded daily requests
                time.sleep(until_midnight())
            elif err.code==401:
                print(err.code, unix_time)
                #invalid api key
                break
            else:
                #print(err, unix_time, 'unavailable data')
                for j in range(limit):
                    with open(path+sym_id+'_'+str(unix_time+j*604800)+'_'+str(unix_time+(j+1)*604800)+'.txt', 'w') as ff:
                        json.dump([],ff)
                #unavailable data
                return( [] )  
    
            
def upload_rates(unix_time, base, quote):
    path='/home/fbuonerba/exchange_rates_data/'
    try:
        with open(path+'exchange_rate_'+str(base)+'_'+str(quote)+'_'+str(unix_time)+'.txt') as json_file:
            exchange = json.load(json_file)    
    except:
        exchange=request_rates(unix_time, base, quote) 
    return(exchange)
    

def upload_ohlcv(unix_time, sym_id, limit):
    path='/home/fbuonerba/ohlcv_data/ohlcv_'
    try:
        with open(path+sym_id+'_'+str(unix_time)+'_'+str(unix_time+86400)+'.txt') as json_file:
            ohlcv = json.load(json_file)    
    except:
        ohlcv=request_ohlcv(unix_time, sym_id, limit)
        if len(ohlcv)>0:
            ohlcv=ohlcv[0]
    #given the structure, if no data is available there is [], otherwise its a list with 1 entry.
    return(ohlcv)

def upload_ohlcv_weekly(unix_time,sym_id):
    path='/home/fbuonerba/ohlcv_data/ohlcv_'
    try:
        with open(path+sym_id+'_'+str(unix_time)+'_'+str(unix_time+604800)+'.txt') as json_file:
            ohlcv = json.load(json_file)    
    except:
        ohlcv=request_ohlcv_weekly(unix_time, sym_id) 
    return(ohlcv)
    

def compute_log_return(unix_time, base, quote, interval):
    ret1=upload_rates(unix_time,base,quote)
    ret2=upload_rates(unix_time+interval,base,quote)
    if ret1=={} or ret2=={}:
        log_ret=float('nan')
    else:
        log_ret=np.log(ret2['rate'])-np.log(ret1['rate'])
    path2='/home/fbuonerba/log_returns_data/log_return_'
    name=path2+str(base)+'_'+str(quote)+'_'+str(unix_time)+'_'+str(unix_time+interval)+'.txt'
    with open(name,'w') as ff:
        json.dump(log_ret,ff)
    return(log_ret)

def upload_log_return(unix_time, base, quote, interval):
    path2='/home/fbuonerba/log_returns_data/log_return_'
    name=path2+str(base)+'_'+str(quote)+'_'+str(unix_time)+'_'+str(unix_time+interval)+'.txt'
    try:
        with open(name) as json_file:
            log_return = json.load(json_file)    
    except:
        log_return=compute_log_return(unix_time, base, quote, interval) 
    return(log_return)

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
    #previous version
    #Supply=[]
    #SoSupply=soup.find_all('span',{'data-supply':True})
    #for x in SoSupply:
    #    x=x.contents[0].strip('\n').replace(',','')
    #    if '?' in x:
    #        x=float('nan')
    #    else:
    #        x=int(float(x))
    #    Supply.append(x)
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
        data[Syms[i]]={'volume': Vol[i], 'price': Price[i], 'supply': Supply[i]}
    with open('/home/fbuonerba/codes/meta_data/new_cmc_id.txt') as ff:
        coins=json.load(ff)
    #reduce the dictionary to include only new_coins.
    #Possible errors if new_coins do not appear in data.keys()
    finaldictio={}
    for c in coins.values():
        try:
            finaldictio[c]=data[c]
        except:
            finaldictio[c]={'volume': float('nan'), 'price': float('nan'), 'supply': float('nan')}
    #create file. Convert date into time since epoch to appear in the file name.
    date=str(date)
    year=int(float(date[:4]))
    month=int(float(date[4:6]))
    day=int(float(date[6:]))
    unix_time=datetime(year,month,day).strftime('%s')
    with open('/home/fbuonerba/cmc_data/cmc_historical_'+str(unix_time)+'.txt','w') as fff:
        json.dump(finaldictio,fff)
    return(finaldictio)

def previous_sunday(t):
    delta=t%604800
    if delta<259200:
        correct=259200-604800-delta
    else:
        correct=259200-delta
    t=t+correct
    return(t)


def upload_historical_coin_number(t, base):
    t=previous_sunday(t)
    with open('/home/fbuonerba/cmc_data/cmc_historical_'+str(t)+'.txt') as ff:
        data=json.load(ff)
    if base=='IOTA':
        coin_no=data['M'+str(base)]['supply']
    else:
        #if error, base is not among coins listed on cmc.
        try:
            coin_no=data[str(base)]['supply']
        except Exception as e:
            coin_no=float('nan')
    return(coin_no)

def upload_coin_number(timee, base):
    t_critical=1532044800#before this threshold, no daily cmc data
    if timee<t_critical:#get most recent Sunday for old files
        coin_no=upload_historical_coin_number(timee, base)
    else:#more recent dates, can try daily cmc data
        try:
            with open('/home/fbuonerba/cmc_data/cmc_'+str(base)+'_'+str(timee)+'.txt') as ff:
                data=json.load(ff)
            try:
                coin_no=data['circulating_supply']
            except Exception as e:
                coin_no=float('nan')
        except:#for some reason there is a hole in daily cmc data - use last sunday
            coin_no=upload_historical_coin_number(timee, base)
    return(coin_no)
    
####Computing factor returns. Eventually might want exponential weighted decay.####   
def compute_returns_variance(base, quote, begin, end, freq):
    #Variance of log_returns over perios of time.
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'_'+str(freq)
    t=begin
    returns=[]
    #collect returns with frequency=freq
    while t<=end+1:
        ret=upload_log_return(t,base,quote,freq)
        #ret is a number
        if np.isnan(ret)==False:
            returns.append(ret)
        t+=freq
    if returns==[]:
        variance=0
    else:
        variance = np.var(np.array(returns))
        print(base, quote, 'var=',variance)
    with open('/home/fbuonerba/factor_loadings/variance_'+sym+'.txt','w') as ff:
        json.dump(variance, ff)
    return(variance)


def compute_rates_high_low(base, quote, begin, end, freq):
    #log( max(rates)/min(rates) )
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'_'+str(freq)
    t=begin
    rates=[]
    #collect rates with frequency=freq
    while t<=end+1:
        rat=upload_rates(t,base,quote)
        #rat is a dictionary
        if rat!={}:
            rates.append(rat['rate'])
        t+=freq
    if rates==[]:
        high_low=0
    else:
        rr=np.array(rates)
        high_low = np.log((np.max(rr))/(np.min(rr)))
    print(base, quote, 'highlow=', high_low)
    with open('/home/fbuonerba/factor_loadings/high_low_'+sym+'.txt','w') as ff:
        json.dump(high_low, ff)
    return(high_low)

def compute_returns_strength(base, quote, begin, end, freq):
    # sum_t ( log( 1 + return_t))
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'_'+str(freq)
    t=begin
    returns=[]
    #collect returns, only if not NaN
    while t<=end+1:
        ret=upload_log_return(t,base,quote,freq)
        #ret is a number
        if np.isnan(ret)==False:
            returns.append(ret)
        t+=freq
    if returns==[]:
        strength=0
    else:
        arr=1+np.array(returns)
        arr=arr[arr>0]
        if arr==[]:
            strength=0
        else:
            strength=np.sum(np.log(arr))
    print(base, quote, 'str=', strength)
    with open('/home/fbuonerba/factor_loadings/strength_'+sym+'.txt','w') as ff:
        json.dump(strength, ff)
    return(strength)  

def compute_log_marketcap(base, quote, begin, end):
    #average log( price x coin_supply )
    # start Jan07=1515283200
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)
    t=begin
    mkcap=[]
    #collect coin market caps, only if coin_no not NaN and rates non-empty
    while t<=end + 1:
        coin_no=upload_coin_number(t, base)
        rate=upload_rates(t, base, quote)
        #rate is a dictionary
        if rate!={} and np.isnan(coin_no)==False:
            mkcap.append(coin_no*rate['rate'])
        t+=86400
    if mkcap==[]:
        log_mkcap=0
    else:
        log_mkcap=np.log(np.mean(np.array(mkcap)))
    print(base, quote, 'log_mkcap=', log_mkcap)
    with open('/home/fbuonerba/factor_loadings/log_mkcap_'+sym+'.txt','w') as ff:
        json.dump(log_mkcap, ff)
    return(log_mkcap)  

def compute_log_marketcap_exact(base,quote,timee):
    #log( price x coin_supply )
    #cmc_data not available daily since jan07 - hence if before a critical
    #time T=1532044800, round to most recent Sunday, else use daily.
    sym=str(base)+'_'+str(quote)+'_'+str(timee)
    coin_no=upload_coin_number(timee, base)
    rate=upload_rates(timee, base, quote)
    #rate is a dictionary
    if rate!={} and np.isnan(coin_no)==False:
        mkcap=coin_no*rate['rate']
    else:
        mkcap=0
    print(base, quote, 'log_mkcap=', mkcap)
    with open('/home/fbuonerba/factor_loadings/log_mkcap_exact_'+sym+'.txt','w') as ff:
        json.dump(mkcap, ff)
    return(mkcap)
    
def compute_average_coin_number(coin, begin, end):
    t_critical=1532044800
    t=begin
    daily_coins=[]
    while t<end:
        coin_no=upload_coin_number(t, coin)
        daily_coins.append(coin_no)
        t+=86400
    daily_coins=np.array(daily_coins)
    mean=np.mean(daily_coins)
    return(mean)

def compute_turnover_exact(base, quote, begin, end):
    #total coins traded in time frame/average supply
    coin_no=compute_average_coin_number(base, begin, end)
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)
    ratepath='/home/fbuonerba/exchange_rates_data/exchange_rate_'
    t=begin
    traded_coins=0
    pool=mp.Pool()
    with open('/home/fbuonerba/codes/meta_data/new_symbols.txt') as ff:
        symbols=json.load(ff)
    it_symbols=[]
    #pick symbols with required base and quote from all coinapi symbols.
    for symbol in symbols:
        if str(base)+'_'+str(quote) in symbol:
            it_symbols.append(symbol)
    while t<=end + 1:
        vol=0
        results=[pool.apply_async(upload_ohlcv, args=(t,symbol,1,)) for symbol in it_symbols]
        output=[res.get() for res in results]        
        for out in output:
            if (out!=[] and out!={}):
                vol+=out['volume_traded']#total volume traded in BTC during the day
        rate=upload_rates(t, base, quote)
        if rate!={}:
            traded_coins+=vol/rate['rate']
        t+=86400
    pool.close()#this is to avoid overloading memory
    pool.join()
    turnover=traded_coins/coin_no
    print(base, quote, 'turnover=',turnover)
    with open('/home/fbuonerba/factor_loadings/exact_turnover_'+sym+'.txt','w') as ff:
        json.dump(turnover, ff)
    return(turnover)  
        

def compute_turnover(base, quote, begin, end):
    #total_traded_volume_in_BTC/average_coin_supply 
    # start Jan07=1515283200
    coin_no=compute_average_coin_number(base, begin, end)
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)
    t=begin
    with open('/home/fbuonerba/codes/meta_data/new_symbols.txt') as ff:
        symbols=json.load(ff)
    it_symbols=[]
    #pick symbols with required base and quote from all coinapi symbols.
    for symbol in symbols:
        if str(base)+'_'+str(quote) in symbol:
            it_symbols.append(symbol)
    vol=0
    pool=mp.Pool()
    while t<=end:
        results=[pool.apply_async(upload_ohlcv, args=(t,symbol,1,)) for symbol in it_symbols]
        output=[res.get() for res in results]        
        for out in output:
            if (out!=[] and out!={}):
                vol+=out['volume_traded']
        t+=86400
    pool.close()#this is to avoid overloading memory
    pool.join()
    turnover=vol/coin_no
    print(base, quote, 'turnover=', turnover)
    with open('/home/fbuonerba/factor_loadings/naive_turnover_'+sym+'.txt','w') as ff:
        json.dump(turnover, ff)
    return(turnover)  

def upload_turnover_naive(base,quote,begin,end):
    path='/home/fbuonerba/factor_loadings/naive_turnover_'
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'.txt'
    try:
        with open(path+sym) as file:
            turnover=json.load(file)
    except:
        turnover=compute_turnover(base,quote,begin,end)
    return(turnover)

def compute_coin_ratio(base, begin, end):
    #pick a recent file to see max number of coins ever.
    #If it doesn't exit, return 0 as coin is not listed on cmc.
    try:
        with open('/home/fbuonerba/cmc_data/cmc_'+str(base)+'_1534896000.txt') as iif:
            dat=json.load(iif)
        max_coins=dat['max_supply']
    except Exception as e:
        print(e, base)
        max_coins=None
    if max_coins==None:
        coin_ratio=0
    else:
        t=begin
        weekly_coins=[]
        #get weekly number of coins in circulation:
        while t<=end+1:
            with open('/home/fbuonerba/cmc_data/cmc_historical_'+str(t)+'.txt') as uuf:
                data=json.load(uuf)
            if base=='IOTA':
                weekly_supply=data['MIOTA']['supply']
            else:
                weekly_supply=data[str(base)]['supply']
            weekly_coins.append(weekly_supply)
            t+=604800 
        #compute mean supply over period
        coin_ratio=np.mean(np.array(weekly_coins))/max_coins
    with open('/home/fbuonerba/factor_loadings/coin_ratio_'+str(base)+'.txt','w') as ff:
        json.dump(coin_ratio,ff)
    return(coin_ratio)  

def compute_coin_ratio_exact(base, timee):
    try:
        with open('/home/fbuonerba/cmc_data/cmc_'+str(base)+'_1534896000.txt') as iif:
            dat=json.load(iif)
        max_coins=dat['max_supply']
    except Exception as e:
        print(e, base)
        max_coins=None
    if max_coins==None:
        coin_ratio=0
    else:
        with open('/home/fbuonerba/cmc_data/cmc_historical_'+str(timee)+'.txt') as uuf:
            data=json.load(uuf)
        if base=='IOTA':
            supply=data['MIOTA']['supply']
        else:
            supply=data[str(base)]['supply']    
        coin_ratio=supply/max_coins
    with open('/home/fbuonerba/factor_loadings/coin_ratio_exact_'+str(base)+'_'+str(timee)+'.txt','w') as ff:
        json.dump(coin_ratio,ff)
    return(coin_ratio)
        
def compute_factor_loadings(base,quote,begin,end,freq):
    #frequency for factors involving coin supply is one week.
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'_'+str(freq)
    dictionary={}
    dictionary['returns_variance']=compute_returns_variance(base,quote,begin,end,freq)
    dictionary['rates_high_low']=compute_rates_high_low(base,quote,begin,end,freq)
    dictionary['returns_strength']=compute_returns_strength(base,quote,begin,end,freq)
    dictionary['log_marketcap']=compute_log_marketcap(base,quote,begin, end)
    dictionary['turnover']=upload_turnover_naive(base,quote,begin,end)
    #dictionary['coin_ratio']=compute_coin_ratio(base,begin,end)
    sys.stdout.flush()#force print
    with open('/home/fbuonerba/factor_loadings/averaged_factors_'+sym+'.txt','w') as file:
        json.dump(dictionary,file)
    return(dictionary)
        
def upload_factor_loadings(base,quote,begin,end,freq):
    sym=str(base)+'_'+str(quote)+'_'+str(begin)+'_'+str(end)+'_'+str(freq)
    try:
        with open('/home/fbuonerba/factor_loadings/factors_'+sym+'.txt') as file:
            factor_loadings=json.load(file)
    except:
        factor_loadings=compute_factor_loadings(base,quote,begin,end,freq)
    return(factor_loadings)


    
    

    
    
