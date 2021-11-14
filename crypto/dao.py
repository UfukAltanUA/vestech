from sqlalchemy import create_engine
import cx_Oracle
from pandas import read_sql_query, to_sql

from config import db_username, db_password, database, url, location

class Database():
	
	cx_Oracle.init_oracle_client(lib_dir = location)
	engine_path = 'oracle+cx_oracle://' + db_username + ':' + db_password + '@' + url + ':1521/?service_name=' + database

	def __init__(self):
		self.engine = create_engine(engine_path)

    def get_balance(self):

	    data = read_sql_query('SELECT * FROM UFUK.BARIS', self.engine)
        return data

    def post_balance(self, row, ):
        
        data = read_sql_query('SELECT * FROM UFUK.BARIS', self.engine)




price = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
new_balance = price * quantity

data.columns

result = {ticker: new_balance, 'Price': 10.0}
		

df2 = df.append(dictionary, ignore_index = True)


