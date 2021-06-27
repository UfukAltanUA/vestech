from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from ta.momentum import StochRSIIndicator

def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])
    
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    #heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    
    #heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    
    return heikin_ashi_df

def stochastic_rsi(price):
    
    srsi = StochRSIIndicator(price)
    d = srsi.stochrsi_d()
    k = srsi.stochrsi_k()

    return d, k

def stockhastic_rsi_signal(stock):
    signal = []
    for i in range(0, len(stock)):
        if stock['%K'][i] > stock['%D'][i] and stock['%K'][i] < .2:
            signal.append(True)
        elif stock['%K'][i] < stock['%D'][i] and stock['%D'][i] > .8:
            signal.append(False)
        else:
            signal.append('Unknown')
    
    return signal

def bollinger_bands(stock):

    stock['TP'] = (stock['high'] + stock['low'] + stock['close']) / 3
    stock['STD'] = stock['TP'].rolling(20).std(ddof = 0)
    stock['MA-TP'] = stock['TP'].rolling(20).mean()

    stock['BOLU'] = stock['MA-TP'] + 2 * stock['STD']
    stock['BOLD'] = stock['MA-TP'] - 2 * stock['STD']
    stock.drop(['TP', 'MA-TP'], axis = 1, inplace = True)
    
    return "Bollinger Bands Calculated"

def bollinger_bands_signal(stock):
    
    signal = []
    for i in range(0, len(stock)):
        if stock['BOLD'][i] > stock['low'][i]:
        #if stock['BOLD'][i] / stock['Low'][i] > .96 or stock['BOLD'][i] / stock['Low'][i] < 1.04:
            signal.append(True)
        else:
            signal.append('Unknown')
    stock['BBL'] = signal