from service import tickers
import service
from datetime import datetime, timedelta
from pandas_datareader import get_data_yahoo
import schedule
from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
import time
s = time.time()

end = datetime.today() #- timedelta(days = 5)
start = end - timedelta(days = 36)

df = get_data_yahoo(tickers, start, end)

close = df['Close']
high = df['High']
low = df['Low']
_open = df['Open']

cols = {'close':close, 'high': high, 'low': low, 'open': _open}

results = service.process_stocks(tickers, cols)

data = pd.DataFrame(results, columns = ['Tickers', 'Price', 'HA', 'BB', 'SRSI']) 
data = data.sort_values('Tickers', ascending = True)

service.write_into_excel(data)
service.send_document()

e = time.time()

print(e-s)

# Read Articles
# Bollinger Bands, RSI Research
# TEMA, Stockhastic RSI
# Probabilities of each situation to increase and decrease in value
# Saving previous results ---->  ???????
# Evaluating last few days of trend
# 

"""
from time import sleep

#for i in ["11:40", "14:00", "17:00"]:

schedule.every().sunday.at("17:55").do(automate)

while True:
    schedule.run_pending()
    sleep(1)

"""


# anaconda python				+
# sublime text vs visual studio	+
# Git bash						
# VPN							
# discord						+
# investing						+
# requirements.txt  			+
# postman						+
# education						
# 


# hadoop