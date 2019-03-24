import datetime
import redis
import time
import argparse
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

# read arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--api_key', help='api key for accessing alpha vantage.')
parser.add_argument('--symbol', help='stock symbol to subscribe to.')
args = parser.parse_args()
api_key = args.api_key
symbol = args.symbol

# get data from alpha vantage api.
data = TimeSeries(key = api_key, output_format = 'pandas')
ts_data, ts_meta_data = data.get_intraday(symbol = symbol, interval = '1min', outputsize = 'compact')
ts = ts_data["4. close"]
ts.columns = ["price"]

# establish Redis connection; select database: 1
r = redis.Redis( host=u'localhost', port=6379, db=1 )

# load data inside redis.
# save at the 20 & 50 second point in the minute (update new data points every 30 seconds).
sec = datetime.now().second
time.sleep( ( 60 - sec - 10 ) % 30 )

ts_name = "ts_" + symbol
ts_ix = ts.index
ts_dict = {}
for ix in ts_ix:
	ix_time = datetime.strptime(ix, "%Y-%m-%d %H:%M:%S")
	ix_timestamp = int(datetime.timestamp(ix_time))
	v = str(ix_timestamp) + "_" + str(ts[ix])
	ts_dict[v] = ix_timestamp
r.zadd(ts_name, ts_dict)

# update mongodb every 2 hours
