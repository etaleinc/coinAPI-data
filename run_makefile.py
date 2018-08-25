import subprocess
import json
import time
import multiprocessing as mp

def worker1(unix_time, base, quote):
    pro=subprocess.Popen(["make", "--file=Makefile", "unix_time=%s" % unix_time, "base=%s" % base, "quote=%s" % quote, "interval=" %interval])

def worker2(unix_time,sym_id):
    pro=subprocess.Popen(["make", "--file=Makefile2", "unix_time=%s" % unix_time, "sym_id=%s" % sym_id])
    

with open('/home/fbuonerba/codes/meta_data/new_coins.txt') as f:
    coins=json.load(f)
quotes=['USD','BTC']
with open('/home/fbuonerba/codes/meta_data/new_symbols.txt') as ff:
    symbols=json.load(ff)
#get beginning of current hour
T=time.time()
unix_time=T-T%3600
pool=mp.Pool()
interval=86400
results1=[pool.apply_async(worker1, args=(unix_time-interval,base,quote,interval,) ) for base in coins for quote in quotes]

results2=[pool.apply_async(worker2, args=(unix_time-interval,sym_id,) ) for sym_id in symbols]



#without pro.wait(), results(time=t) are started even if results(time=t-1) is not done.    
#make -s : only error outputs.


# unix_time=1532458800
# interval=3600
# pool = mp.Pool()
# while True:
#     results=[pool.apply_async(worker, args=(unix_time,base,quote,interval,) ) for base in coins for quote in quotes ]
#     unix_time+=3600
#     #Even though after time.time() every worker sleeps, this loop keeps creating workers.
#     #It needs to be forced to sleep along with actual workers.
#     #results is detatched and runs in parallel with the 'if' below.
#     if unix_time>=time.time():
#         time.sleep(unix_time - time.time() + 5)
    


