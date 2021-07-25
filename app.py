from service import tickers
import service
from datetime import datetime, timedelta
#import schedule
from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
import time

s = time.time()

results = service.process_stocks(tickers)

data = pd.DataFrame(results, columns = ['Tickers', 'Price', 'BB', 'SRSI', 'RSI', 'TEMA']) 
data = data.sort_values('Tickers', ascending = True)

service.write_into_excel(data)
service.send_document()

e = time.time()

print(e-s)

# Probabilities of each situation to increase and decrease in value

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
# Git bash						+
# VPN							
# discord						+
# investing						+
# requirements.txt  			+
# postman						+
# hadoop