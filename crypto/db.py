from sqlalchemy import create_engine
import cx_Oracle
import pandas as pd

db_username = 'bill1oners'
db_password = 'milli0ners'
service_name = 'ORCLCDB.localdomain'
url = 'localhost'
location = r'/Library/oracle'

cx_Oracle.init_oracle_client(lib_dir = location)
engine_path = 'oracle+cx_oracle://' + db_username + ':' + db_password + '@' + url + ':1521/?service_name=' + service_name
engine = create_engine(engine_path)
data = pd.read_sql_query('SELECT * FROM UFUK.BARIS', engine)

print(data)




