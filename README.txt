* Historical data is stored in directories with names ending in '/home/fbuonerba/..._data'. For example, exchange rates are in exchange_rates_data. Raw data is in json format. By default, files corresponding to unavailable data contain only '{}'.

* The codes used to download the data are in the directory '/home/fbuonerba/codes'.

* The file coinapi_v1.py contains various functions provided by coinAPI to contact their server.

* The file mp_functions.py contains all the functions that implement an elementary step in the data pipeline.

* Functions whose name begins in 'request_' aim at downloading a unit of corresponding data from coinAPI, while handling possible errors. More precisely, the function sends a request to coinAPI. If data is available, the function downloads it and stores it in a file; if data is not available now, but may nonetheless be available in the future, the function sleeps for a while, then tries again to download; otherwise, data is simply not available.

* The programs whose name begins in 'get_' iterate the corresponding function 'request_' , imported from mp_functions.py, over periods of time. They provide the most primitive tool to import historical data. In order to speed up the process, they execute multiple requests in parallel.

* The programs whose name begins in 'upload_' open files with corresponding data and prepare it for further manipulation. More precisely, they first try to open a file; it such file does not exist, they call corresponding 'request_' function and donwload the data.

* The programs whose name begins in 'compute_' transform data from one form to another. For example, compute_log_returns.py loads exchange rates via 'upload_rates' function, and then transforms it into log returns. If data is not available, the corresponding file contains 'NaN'.

* Makefile controls the pipeline of data transformation. At the present time, it only loads exchange rates and dumps log returns: 'compute_log_returns' calls 'upload_rates' which calls 'request_rates'.

* run_makefile.py manages execution of Makefile via python script. In order to speed up the process, it executes multiple makefiles in parallel.

* The directory 'meta_data' contains files featuring names of coins, exchanges, etc. etc.

* The directory 'ipynotebooks' contains python notebooks used to test codes.

* The directory 'obsolete' contains old and naive versions of the codes.



