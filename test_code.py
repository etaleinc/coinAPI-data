import sys
sys.path.insert(0, '/home/fbuonerba')
from data_try_except import get_symbols, get_assets, request_exchange_rates, until_midnight
#unix_time= 1451606400
assets=get_assets()
#Loop to download data: keep sending requests. 
#if some problem appears during a request, the problem
#is in request_exchange_rates, and the function will pause
unix_beginning= 1504186800
while True:
    request_exchange_rates(unix_beginning, 'BTC', 'USD')
    unix_beginning+=3600

