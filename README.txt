* Historical data is stored in directories with names ending in '/home/fbuonerba/..._data'. For example, exchange rates are in exchange_rates_data. Raw data is in json format. By default, files corresponding to unavailable data contain only '{}'.

* The codes used to download the data are in the directory '/home/fbuonerba/codes'.

* Both exchange rates and ohlcv come from coinAPI, while cmc_data is taken from CoinMarketCap.
Unfortunately ohlcv is a bit tricky to use: a single request requires we specifiy a triple (base,quote,exchange), so it is impossible to get, e.g. total traded volume for a given coin in a single request. Further, volumes are recorded in units of base coin - however this is not true for BITMEX, and maybe for other exchanges too...   

* The file 'get_cmc_data.py' downloads 24h-traded_volumes, number of coins available, and other data, from CoinMarketCap. It is automated to operate once a day, at 00.01, via crontab.

* The file coinapi_v1.py contains various functions, provided by coinAPI on GitHub, to contact their server.

* The file mp_functions.py contains all the functions that implement an elementary step in the data pipeline. In detail:

* Functions whose name begins in 'request_' aim at downloading a unit of corresponding data from coinAPI, while handling possible errors. More precisely, the function sends a request to coinAPI. If data is available, the function downloads it and stores it in a file; if data is not available now, but may nonetheless be available in the future, the function sleeps for a while, then tries again to download; otherwise, data is simply not available.

* The programs whose name begins in 'get_' iterate the corresponding function 'request_' , imported from mp_functions.py, over periods of time. They provide the most primitive tool to import historical data. In order to speed up the process, they execute multiple requests in parallel.

* The programs whose name begins in 'upload_' open files with corresponding data and prepare it for further manipulation. More precisely, they first try to open a file; it such file does not exist, they call corresponding 'request_' function to donwload the data.

* The programs whose name begins in 'compute_' transform data from one form to another. For example, compute_log_returns.py loads exchange rates via 'upload_rates', and then transforms it into log returns. If data is not available, the corresponding file contains 'NaN'.

* Makefile controls the pipeline of data transformation. At the present time, it only loads exchange rates and dumps log returns: 'compute_log_returns' calls 'upload_rates' which calls 'request_rates'.

* run_makefile.py manages execution of Makefile via python script. In order to speed up the process, it executes multiple makefiles in parallel.

* The directory 'meta_data' contains files featuring names of coins, exchanges, etc. etc.

* The file 'top_coins.txt' lists all coins we analyze. The file 'symbols.txt' contains those triples (exchange, base, quote) with base in 'top_coins.txt', quote = 'USD' or 'BTC', for which coinAPI has data. The file 'cmc_id_list.txt' contains a dictionary of coins in top_coins, together with their id_number from CoinMarketCap.

*Remark that coins listed in 'top_coins.txt' and those in 'cmc_id_list.txt' differ - the second is a subset of the first, with difference 'EUR','AIO','LIZA','HB' - unquestionably mysterious coins.

* The directory 'ipynotebooks' contains python notebooks used to test codes and make quick experiments.


