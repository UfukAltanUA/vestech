import utils
import smtplib
from email.message import EmailMessage
from warnings import filterwarnings
filterwarnings('ignore')
import pandas as pd
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

tickers = ['AEFES.IS', 'AKBNK.IS', 'AKSA.IS' , 'AKGRT.IS', 'ARCLK.IS', 'ASELS.IS', 'AYGAZ.IS',
           'BIZIM.IS', 'BRISA.IS', 'BANVT.IS', 'VESBE.IS', 'CCOLA.IS', 'CIMSA.IS', 'CLEBI.IS',
           'VAKBN.IS', 'VESTL.IS', 'YKBNK.IS', 'ZOREN.IS', 'TCELL.IS', 'THYAO.IS', 'KOZAA.IS',
           'ISCTR.IS', 'DOAS.IS' , 'DOHOL.IS', 'ECILC.IS', 'ECZYT.IS', 'EKGYO.IS', 'ENJSA.IS', 
           'ENKAI.IS', 'ERBOS.IS', 'FROTO.IS', 'GARAN.IS', 'GOODY.IS', 'GOZDE.IS', 'GUBRF.IS', 
           'HALKB.IS', 'HEKTS.IS', 'HLGYO.IS', 'IPEKE.IS', 'INDES.IS', 'ISDMR.IS', 'ISFIN.IS',
           'KORDS.IS', 'KLMSN.IS', 'KOZAL.IS', 'BIMAS.IS', 'BRSAN.IS', 'BUCIM.IS', 'CEMTS.IS',
           'DEVA.IS' , 'EGEEN.IS', 'EREGL.IS', 'GSDHO.IS', 'ISGYO.IS', 'ISMEN.IS', 'KAREL.IS',
           'KARSN.IS', 'KARTN.IS', 'KCHOL.IS', 'KERVT.IS', 'BFREN.IS', 'GSRAY.IS', 'ARENA.IS',
           'ARMDA.IS', 'ARDYZ.IS', 'SEKFK.IS', 'AKSEN.IS', 'ALARK.IS', 'ALBRK.IS', 'ALKIM.IS',
           'ALGYO.IS', 'ANACM.IS', 'ANHYT.IS', 'GUSGR.IS', 'KRDMD.IS', 'LOGO.IS' , 'MAVI.IS' ,
           'MGROS.IS', 'MPARK.IS', 'NETAS.IS', 'NTHOL.IS', 'ODAS.IS' , 'OTKAR.IS', 'PETKM.IS',
           'PGSUS.IS', 'SAHOL.IS', 'SASA.IS' , 'SISE.IS' , 'SKBNK.IS', 'SODA.IS' , 'SOKM.IS' ,
           'TATGD.IS', 'TAVHL.IS', 'TKFEN.IS', 'TMSN.IS' , 'TOASO.IS', 'TRCAS.IS', 'TRGYO.IS',
           'TRKCM.IS', 'TSKB.IS' , 'TTKOM.IS', 'TTRAK.IS', 'TUPRS.IS', 'ULKER.IS', 'YATAS.IS']

def process_stocks(tickers,cols):
    
    results = []
    
    for ticker in tickers:
        
        dataset = pd.DataFrame()
        
        dataset['close'] = cols['close'][ticker]
        dataset['high'] = cols['high'][ticker]
        dataset['low'] = cols['low'][ticker]
        dataset['open'] = cols['open'][ticker]
        
        utils.bollinger_band_low(dataset)
        utils.bollinger_bands_signal(dataset)

        if ticker == 'EREGL.IS':
          print('BOLD')
          print(dataset['BOLD'][-1])
          print(dataset['BOLD'][-1]  * 1.01 )
          print(dataset['low'][-1])
        
        dataset['%D'], dataset['%K'] = utils.stochastic_rsi(dataset['close'])
        dataset['SRSI'] = utils.stockhastic_rsi_signal(dataset)
        
        utils.tema(dataset)
        utils.tema(dataset, span = 21)
        dataset['TEMASignal'] = utils.tema_signal(dataset)
        
        dataset_ha = utils.heikin_ashi(dataset)
        
        bearish_engulfing_signal = utils.bearish_engulfing(dataset)
        
        ha_close = dataset_ha['close'].iloc[-1]
        ha_open = dataset_ha['open'].iloc[-1]
        ha_close2 = dataset_ha['close'].iloc[-2]
        ha_open2 = dataset_ha['open'].iloc[-2]
        
        if  ha_close > ha_open  and ha_close2 <= ha_open2:
            ha_signal = True
            
        elif ha_close < ha_open and ha_close2 >= ha_open2:            
            ha_signal = False
            
        else:
            ha_signal = 'Unknown'
            
        srsi_signal = dataset['SRSI'].iloc[-1]
        bb_signal = dataset['BBL'].iloc[-1]
        price = dataset['close'].iloc[-1]
        tema_sgnl = dataset['TEMASignal'].iloc[-1]
        
        results.append([ticker, price, ha_signal, bb_signal, srsi_signal, tema_sgnl, bearish_engulfing_signal])
            
    return results

def write_into_excel(data):

      writer = pd.ExcelWriter('report.xlsx', engine = 'xlsxwriter')
      data.to_excel(writer, sheet_name = 'VestechSolutions')

      workbook = writer.book
      worksheet = writer.sheets['VestechSolutions']

      green = workbook.add_format({'bg_color': '#b2e3a1', 'font_color': '#ffffff'}) 
      red = workbook.add_format({'bg_color': '#ba240d', 'font_color': '#ffffff'}) 

      # HA
      worksheet.conditional_format('D2:D106', {'type': 'cell', 'criteria': '=', 'value': True, 'format': green})
      worksheet.conditional_format('D2:D106', {'type': 'cell', 'criteria': '=', 'value': False, 'format': red})

      # BB
      worksheet.conditional_format('E2:E106', {'type': 'cell', 'criteria': '=', 'value': True, 'format': green})
      worksheet.conditional_format('E2:E106', {'type': 'cell', 'criteria': '=', 'value': False, 'format': red})

      # SRSI
      worksheet.conditional_format('F2:F106', {'type': 'cell', 'criteria': '=', 'value': True, 'format': green})
      worksheet.conditional_format('F2:F106', {'type': 'cell', 'criteria': '=', 'value': False, 'format': red})      

      # TEMA
      worksheet.conditional_format('G2:G106', {'type': 'cell', 'criteria': '=', 'value': True, 'format': green})

      # BES
      worksheet.conditional_format('G2:G106', {'type': 'cell', 'criteria': '=', 'value': False, 'format': red})

      writer.close()    

def send_document(filename = 'report.xlsx', to = 'ufukaltan08@gmail.com', host='smtp.gmail.com', subject = 'Bist Report'):
    email = MIMEMultipart()
    email['from'] = 'Ufuk Altan'
    email['to'] = to
    email['subject'] = subject

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("report.xlsx", "rb").read())
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', 'attachment; filename = "report.xlsx"')
    email.attach(part)
    
    with smtplib.SMTP(host = host, port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('ufukaltanua@gmail.com', 'zingoqnwwcrwncag')
        smtp.send_message(email)

def send_email(document, to = 'ufukaltan08@gmail.com', host='smtp.gmail.com', subject = 'Borsa'):
    email = EmailMessage()
    email['from'] = 'Ufuk Altan'
    email['to'] = to
    email['subject'] = subject
    email.set_content(document) 
    
    with smtplib.SMTP(host = host, port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('ufukaltanua@gmail.com', 'zingoqnwwcrwncag')
        smtp.send_message(email)
