from mp_functions import compute_log_return
import sys
unix_time=int((sys.argv[1]))
base=sys.argv[2]
quote=sys.argv[3]
interval= int(sys.argv[4])
compute_log_return(unix_time, base, quote, interval)
