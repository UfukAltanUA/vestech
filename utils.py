from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from ta.momentum import StochRSIIndicator
from ta.volatility import BollingerBands
from ta.trend import ADXIndicator
import numpy as np

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
        if stock['BOLD'][i]  * 1.01 > stock['low'][i]  and stock['close'][i] > stock['open'][i]:
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

    for i in range(0, len(stock)):

        if stock['close'][i] * 1.03 <= stock['open'][i]:
            signal.append(False) 
        else:
            signal.append('Unknown')
         
    return signal
    
def average_directional_index(dataset):

    high = pd.Series(np.reshape(dataset['high'].values, (dataset.shape[0],)))
    low = pd.Series(np.reshape(dataset['low'].values, (dataset.shape[0],)))
    close = pd.Series(np.reshape(dataset['close'].values, (dataset.shape[0],)))

    adxI = ADXIndicator(high, low, close, 14, True)
    pos = adxI.adx_pos()
    neg = adxI.adx_neg()
    #adx = adxI.adx()

    dataset['-DI'] = list(neg)
    dataset['+DI'] = list(pos)
    #dataset['ADX'] = list(adx)

def di_signal(stock, threshold = 2.6):

    signal = []

    for i in range(0, len(stock)):

        if stock['-DI'][i] > stock['+DI'][i] and (stock['-DI'][i] / stock['+DI'][i]) > threshold:
            
            signal.append(True) 
            
        elif stock['+DI'][i] > stock['-DI'][i] and (stock['+DI'][i] / stock['-DI'][i]) > threshold:

            signal.append(False) 

        else:
            signal.append('Unknown')

    stock['ADXSignal'] = signal
