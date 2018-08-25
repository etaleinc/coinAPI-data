from mp_functions import upload_rates
import sys

unix_time=int(float(sys.argv[1]))
base=sys.argv[2]
quote=sys.argv[3]
upload_rates(unix_time, base, quote)
