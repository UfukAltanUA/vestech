from sqlalchemy import create_engine
import cx_Oracle
from pandas import read_sql_query, to_sql

from config import db_username, db_password, database, url, location

class Database():
	
	cx_Oracle.init_oracle_client(lib_dir = location)
	engine_path = 'oracle+cx_oracle://' + db_username + ':' + db_password + '@' + url + ':1521/?service_name=' + database

	def __init__(self):
		self.engine = create_engine(engine_path)

    def get_balance(self, ticker):

	    sql_data = read_sql_query('SELECT * FROM UFUK.BARIS', self.engine)
	    balance_on_db = sql_data[ticker.lower()].iloc[-1]

        return balance_on_db

    def post_balance(self, quantity, ticker):
        
		price = self.client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
		new_balance = price * quantity
        
        sql_data = read_sql_query('SELECT * FROM UFUK.BARIS', self.engine) ???????????
		last_balance = dict(sql_data.iloc[-1])
		last_balance[ticker.lower()] = new_balance
		sql_data = sql_data.append(last_balance, ignore_index = True)
		sql_data.to_sql('UFUK.BARIS', self.engine.connect(), if_exists='replace') ????????



