import subprocess
import json
import time

with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as f:
    coins=json.load(f)
with open('/home/fbuonerba/codes/meta_data/top_exchanges.txt') as ff:
    exchanges=json.load(ff)
quotes=['USD','BTC']

#unix_time=1487379600
#base='LIZA'
#quote='USD'
#interval=3600
#pro=subprocess.Popen(["make","--silent", "unix_time=%s" % unix_time, "base=%s" % base, "quote=%s" % quote, "interval=%s" % interval])

unix_time=1511467200
#1485205200
interval=3600
while True:
    for base in coins:
        for quote in quotes:
            pro=subprocess.Popen(["make", "--silent", "unix_time=%s" % unix_time, "base=%s" % base, "quote=%s" % quote, "interval=%s" % interval])
####subprocess.popen operates its argument as unix command.
####pro.communicate()[0]
    unix_time+=interval
    if unix_time>=time.time():
        time.sleep( interval +10 )

