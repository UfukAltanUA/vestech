from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET

from pandas import DataFrame
from datetime import datetime, timedelta

import smtplib
from email.message import EmailMessage

from config import email_password, db_username, db_password
#from dao import Database
class Request():
#class Request(Database):

    def __init__(self, api_key, secret_key, tickers):

        self.tickers = tickers
        self.client = Client(api_key, secret_key) #tld = 'us'

    def request_balance(self):

        # GET BALANCE FROM DATABASE
        #Add required information
        #Required conditions
        account = self.client.get_account()
        return account

    def request_crypto_data(self):

        df_list = []
        
        for ticker in self.tickers:
            start = (datetime.today() - timedelta(days = 4)).strftime("%d %b, %Y")
            end = datetime.today().strftime("%d %b, %Y")

            data = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1HOUR, start, end)
            values = [[datetime.fromtimestamp(d[0] / 1000), float(d[4])] for d in data] # Date, Close
            df = DataFrame(values, columns=["Date", 'Close'])
            df_list.append([df, ticker])
        
        return df_list

    def request_order(self, ticker, order_type):

        if order_type == 'BUY':

            # GET BALANCE FROM DATABASE
            #balance_on_db = self.request_balance(ticker)
            balance_on_db = 20

            price = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
            price = float(price[0][4])
            quantity = int(balance_on_db / price)

            order = self.client.create_order(symbol = ticker, side = SIDE_BUY, type = ORDER_TYPE_MARKET, quantity = quantity)

            return 'BOUGHT'

        elif order_type == 'SELL':

            quantity = self.client.get_asset_balance(asset=ticker[:-4])['free'] #ticker[:-4] DOGEUSDT --> DOGE
            quantity = int(float(quantity))

            order = self.client.create_order(symbol = ticker, side = SIDE_SELL, type = ORDER_TYPE_MARKET, quantity = quantity)

            return 'SOLD'

        return 'SOMETHING WRONG'

class Analyze():

    def tema(self, df, span = 13):
        
        ema1 = df['Close'].ewm(span = span ,adjust = False).mean()
        ema2 = ema1.ewm(span = span ,adjust = False).mean()
        ema3 = ema2.ewm(span = span ,adjust = False).mean()
        
        df[f'TEMA{span}'] = (3*ema1)-(3*ema2) + ema3
        
    def tema_signal(self, df, spans = [13, 21]):
        
        signal = []
        
        for i in range(0, len(df)):
            
            if df[f'TEMA{spans[0]}'][i] > df[f'TEMA{spans[1]}'][i] and df[f'TEMA{spans[0]}'][i-1] <= df[f'TEMA{spans[1]}'][i-1]:
                signal.append(True)

            elif df[f'TEMA{spans[0]}'][i] < df[f'TEMA{spans[1]}'][i] and df[f'TEMA{spans[0]}'][i-1] >= df[f'TEMA{spans[1]}'][i-1]:
                signal.append(False)

            else:
                signal.append('Unknown')

        df.drop([f'TEMA{spans[0]}', f'TEMA{spans[1]}'], axis = 1, inplace = True)
        
        return signal

    def create_tema_signal(self, df_list):

        decision = []

        for values in df_list:
            
            df = values[0]
            ticker = values[1]
            
            self.tema(df)
            self.tema(df, span = 21)
            df['TEMASignal'] = self.tema_signal(df)
            signal = df['TEMASignal'].iloc[-1]
            decision.append([ticker, signal])

        return decision

class Notification():

    def send_email(self, document, to = 'ufukaltan08@gmail.com', host='smtp.gmail.com', subject = 'Crypto'):
        email = EmailMessage()
        email['from'] = 'Ufuk Altan'
        email['to'] = to
        email['subject'] = subject
        email.set_content(document) 
        
        with smtplib.SMTP(host = host, port = 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('ufukaltanua@gmail.com', email_password)
            smtp.send_message(email)


        







