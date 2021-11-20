import time
from datetime import datetime

from config import *
from service import Trade

if param == 'execute':

	print(datetime.today())

	ufuk = Trade(ufuk_api_key, ufuk_secret_key, tickers)
	ufuk.order()

if param == 'schedule':

	import schedule

	def application():

		print(datetime.today())

		ufuk = Trade(ufuk_api_key, ufuk_secret_key, tickers)
		ufuk.order()

		baris = Trade(baris_api_key, baris_secret_key, tickers)
		baris.order()

		arthur = Trade(arthur_api_key, arthur_secret_key, tickers)
		arthur.order()

	schedule.every().hour.do(application)

	while True:
	    schedule.run_pending()
	    time.sleep(1)


