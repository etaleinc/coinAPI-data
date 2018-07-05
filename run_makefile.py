import subprocess
import json
with open('/home/fbuonerba/codes/meta_data/top_coins.txt') as f:
    coins=json.load(f)
with open('/home/fbuonerba/codes/meta_data/top_exchanges.txt') as ff:
    exchanges=json.load(ff)
quotes=['USD','BTC']



unix_time=1483228800
interval=3600
while True:
    for (base,quote) in zip(coins, quotes):
        #zip just parallelizes for-loop among multiple lists
        pro=subprocess.Popen(["make","unix_time=%s" % str(unix_time), "base=%s" % base, "quote=%s" % quote, "interval=%s" % str(interval)])
#subprocess.popen operates its argument as unix command.
#pro.communicate()[0]
    unix_time+=interval