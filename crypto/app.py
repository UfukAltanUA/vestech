import time
s = time.time()

from service import Trade
from config import *

ufuk = Trade(ufuk_api_key, ufuk_secret_key, tickers)
ufuk.order()
"""
baris = Trade(baris_api_key, baris_secret_key, tickers)
baris.order()
"""
e = time.time()

print(e-s)


"""
from service import Trade
from config import *
import schedule
import time

def application():

	ufuk = Trade(ufuk_api_key, ufuk_secret_key, tickers)
	ufuk.order()

	baris = Trade(baris_api_key, baris_secret_key, tickers)
	baris.order()

schedule.every().hour.do(application)

while True:
    schedule.run_pending()
    time.sleep(1)

"""



# Decision					+
# Sell - Buy				+
# Inheritance				+
# DB 						
# Dashboard


# BINANCE

# Money on Binance 			+
# Buy DOGE, ETH 			+

# Get account info			+
# Order with python 		+

# PYTHON

# Inheritance - super()		+
# Test buy-sell orders		+
# Exception handling 		+
# decrypt function	
# Email functionality		+

#Oracle

# Read Data
# Post Data
# Balance / Price
# 







