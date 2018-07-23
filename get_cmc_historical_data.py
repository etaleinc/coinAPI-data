from mp_functions import request_cmc_historical
import datetime

t=1515283200
#once a week, since Jan-07 until Jul-15.
while t< 1531612801:
    utc_time = datetime.datetime.utcfromtimestamp(t)
    date=utc_time.strftime("%Y%m%d")
    try:
        request_cmc_historical(date)
    except Exception as e:
        print(date, e, 'problems')
    t+=604800