from utils import Analyze, Request, Notification

from config import key

class Trade(Analyze, Request, Notification):
    
    def __init__(self, api_key, secret_key, tickers):
      
      super().__init__(api_key, secret_key, tickers)

    def apply_analysis(self):

      df_list = self.request_crypto_data()
      decision = self.create_tema_signal(df_list)
      return decision

    def order(self):

      decision = self.apply_analysis()

      for values in decision:
        
        ticker = values[0]
        signal = values[1]

        if signal == True:

          try:
            self.request_order(ticker, 'BUY')
            print(f'Bought {ticker}')

          except:
            self.send_email(document = f'Could Not BUY the {ticker}', to = 'vardarbaris@outlook.com')
            self.send_email(document = f'Could Not BUY the {ticker}')
            
            #from subprocess import call
            #call(["python", "app.py", key])
            
        elif signal == False:

          try:
            self.request_order(ticker, 'SELL')
            print(f'Sold {ticker}')

          except:
            self.send_email(document = f'Could Not SELL the {ticker}', to = 'vardarbaris@outlook.com')
            self.send_email(document = f'Could Not SELL the {ticker}')

            #from subprocess import call
            #call(["python", "app.py", key])
          
        else:
          print(f"No order for {ticker}")



















