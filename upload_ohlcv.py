from mp_functions import upload_ohlcv
import sys
unix_time=int(float(sys.argv[1]))
sym_id=sys.argv[2]

upload_ohlcv(unix_time, sym_id, 1)
