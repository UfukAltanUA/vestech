from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from ta.momentum import StochRSIIndicator, RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import ADXIndicator
import numpy as np

def stochastic_rsi(price):
    
    srsi = StochRSIIndicator(price)
    d = srsi.stochrsi_d()
    k = srsi.stochrsi_k()

    return d, k

def stockhastic_rsi_signal(stock):
    signal = []
    for i in range(0, len(stock['close'])):
        if stock['%K'][i] > stock['%D'][i] and stock['%K'][i] < .2:
            signal.append(True)
        elif stock['%K'][i] < stock['%D'][i] and stock['%D'][i] > .8:
            signal.append(False)
        else:
            signal.append('Unknown')
    
    return signal

def relative_strength_index(price):

    rsi_indicator = RSIIndicator(price)
    rsi_values = rsi_indicator.rsi()

    return rsi_values

def relative_strength_index_signal(stock):

    signal = []

    for i, v in enumerate(range(0, len(stock['close']))):

        if stock['RSIValues'][i] < 35 and (stock['open'][i] / stock['close'][i]) < 1.02:
            signal.append(3)

        elif stock['RSIValues'][i] < 35:
            signal.append(2)

        elif stock['RSIValues'][i-1] * 1.03 <= stock['RSIValues'][i] and stock['RSIValues'][i-1] * 1.03 <= stock['RSIValues'][i-2]:
            signal.append(1)

        else:
            signal.append("Unknown")

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
    
