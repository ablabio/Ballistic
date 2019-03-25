import redis
import time
import argparse
from datetime import datetime
from yahoo_finance_api import YahooFinance as yf

# read arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--symbol', help='stock symbol to subscribe to.')
args = parser.parse_args()
symbol = args.symbol

# get data from yahoo finance.
data = yf(symbol, result_range='1d', interval='1m', dropna='True').result
ts = data.Close

# reformat the data.
ts_name = "ts_" + symbol
ts_ix = ts.index
ts_dict = {}
for ix in ts_ix:
	ix_time = ix.to_pydatetime()
	ix_timestamp = int(datetime.timestamp(ix_time))
	ix_timestamp = ix_timestamp - ix_timestamp % 60 # round the time at minute level.
	v = str(ix_timestamp) + "_" + str(ts[ix])
	ts_dict[v] = ix_timestamp

# save at the 0 second point in the minute (import new data points every 60 seconds).
sec = datetime.now().second
time.sleep( ( 60 - sec ) % 60 )

# establish Redis connection; select database: 1
r = redis.Redis( host=u'localhost', port=6379, db=1 )

# load data inside redis.
r.zadd(ts_name, ts_dict)
print(r.zrange(ts_name, -10, -1, withscores=True))

# update mongodb every 2 hours
