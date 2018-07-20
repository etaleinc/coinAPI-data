import subprocess
import json
import time
import multiprocessing as mp

with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as f:
    coins=json.load(f)
quotes=['USD','BTC']

def worker(unix_time, base,quote, interval):
    pro=subprocess.Popen(["make","-s", "unix_time=%s" % unix_time, "base=%s" % base, "quote=%s" % quote, "interval=%s" % interval])
    pro.wait()
#without pro.wait(), results(time=t) are started even if results(time=t-1) is not done.    
    
unix_time=1522540800
interval=3600
pool = mp.Pool()
while True:
    results=[pool.apply_async(worker, args=(unix_time,base,quote,interval,) ) for base in coins for quote in quotes ]
    unix_time+=3600
    


