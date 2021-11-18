import time
s = time.time()
from datetime import datetime

from service import Trade
from config import *

print(datetime.today())

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

from datetime import datetime

import schedule
import time

def application():

	print(datetime.today())

	ufuk = Trade(ufuk_api_key, ufuk_secret_key, tickers)
	ufuk.order()

	baris = Trade(baris_api_key, baris_secret_key, tickers)
	baris.order()

schedule.every().hour.do(application)

while True:
    schedule.run_pending()
    time.sleep(1)

"""
