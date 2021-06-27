from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from ta.momentum import StochRSIIndicator
from ta.volatility import BollingerBands

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

def bollinger_band_low(stock):
    
    bb = BollingerBands(stock['close'], 20, 2)
    stock['BOLD'] = bb.bollinger_lband()

def bollinger_bands_signal(stock):
    
    signal = []
    for i in range(0, len(stock)):
        if stock['BOLD'][i]  * 1.01 > stock['low'][i]:
        #if stock['BOLD'][i] / stock['Low'][i] > .96 or stock['BOLD'][i] / stock['Low'][i] < 1.04:
            signal.append(True)
        else:
            signal.append('Unknown')
    stock['BBL'] = signal

def tema(stock, span = 13):
    
    ema1 = stock['close'].ewm(span = span ,adjust = False).mean()
    ema2 = ema1.ewm(span = span ,adjust = False).mean()
    ema3 = ema2.ewm(span = span ,adjust = False).mean()
    
    stock[f'TEMA{span}'] = (3*ema1)-(3*ema2) + ema3
    
def tema_signal(stock, spans = [13, 21]):
    
    signal = []
    
    for i in range(0, len(stock)):
        if stock[f'TEMA{spans[0]}'][i] > stock[f'TEMA{spans[1]}'][i] and stock[f'TEMA{spans[0]}'][i-1] <= stock[f'TEMA{spans[1]}'][i-1]:
            signal.append(True)
        else:
            signal.append('Unknown')

    stock.drop([f'TEMA{spans[0]}', f'TEMA{spans[1]}'], axis = 1, inplace = True)
    
    return signal
    
def bearish_engulfing(stock):
    
    signal = []
    
    if stock['close'][-1] * 1.03 <= stock['open'][-1]:
        signal.append(False)
    else:
        signal.append('Unknown')
         
    return signal
    