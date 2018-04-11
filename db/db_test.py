# encoding=utf-8
from db.database import Database

conn = Database('pymysql', {
    'username': 'root',
    'password': 'root',
    'database': 'dao_test',
    'port': 3306,
    'charset': 'utf-8',
    'table_prefix': 'ww_',
})
db = conn.open()

def raw_sql():
    print(db.query('SELECT * FROM user WHERE [[id]] = :id').raw_sql())

raw_sql()
