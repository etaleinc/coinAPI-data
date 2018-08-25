from mp_functions import upload_log_return
import sys
unix_time=int(float(sys.argv[1]))
base=sys.argv[2]
quote=sys.argv[3]
interval=int(float(sys.argv[4]))
upload_log_return(unix_time, base, quote, interval)

