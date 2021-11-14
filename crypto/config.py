import sys
from decrypt import decrypt

key = sys.argv[1]

ufuk_api_key = decrypt(key, b'gAAAAABhjVLPGJsslJBrGUIYfabg0Ke2dH5DugXTr166EgDDCGVpHrXjHx9oaYzS2IZCPHNEsK0Ek35jXLwGkrRFeotgIreDI6YnwxVzxgpEBsU2O3pmTiWe3-w_sg4Jplq_ZAzY_Lnwd6CsgWW1xcUsZ75d4_m2ACfykxSeCHZjy2i1zj0WC0s=')
ufuk_secret_key = decrypt(key, b'gAAAAABhjVOFNu2hk8pxSOEKxPU0tIWcklqkEkI8MNdj-HHU7hdeODGSBkjnvTmccR6kgmirxYinavf9VngpzUqhCmtUepq5k8MIEbsdhpfLDSt_ZY7-WQrXH-uBRvdyO-SsQFQBTIgB9UkNz0gn6GpiI21SxoPBJAvt5IlNbBv5aalFIZBN_pE=')

baris_api_key = decrypt(key, b'gAAAAABhjVO7nyafz438dO0prDq6prdOJfGymhXk2TMRkt689eKDH3ylA0GjbQVqcAraWYrKdZa5ZGx4uLXdHOPNdv8Tc4KFiU16FbBtbacer9iMHB58otodQG9_BGHdD_H75Zg4w2T34GWSZ0AtIoLUs0U7UEQyvtamgDLqdtp2SxJX_3zjbHA=')
baris_secret_key = decrypt(key, b'gAAAAABhjVPsLmT_1pn97q8ebiXMrZUT6IibRbqLp5po9PCFacw_f_H0eREMQp9wDEndB08cDpc1jyliEo5J69xXxlOZMxB8eVWpwF1KI9xvNrWt22kce50DMKrwJUbPs4VbOzHpbFVjAH1r8FjIzGUVfUudrrj_lRnmrZOtGSYnMIy67lEMFRE=')

email_password = decrypt(key, b'gAAAAABhjVWfd65GHZ038GKhe2jkneC2HfwZ5XQJcTgoZb1XU5tBDPACCacPhmQwy-KwrMLU82jFuKcmoJdfeDVhZkVXDg6lDm_BEPIYKi9az2Dvtn7zEow=')

tickers = ['ADAUSDT', 'FTMUSDT', 'DOGEUSDT']

db_username = 'bill1oners'
db_password = 'milli0ners'

database = 'ORCLCDB.localdomain'
url = 'localhost'
location = r'/Library/oracle'
