# encoding=utf-8
from db.database import Database

db = Database('pymysql', {
    'username': 'root',
    'password': 'root',
    'database': 'dao_test',
    'port': 3306,
    'charset': 'utf-8',
    'table_prefix': 'ww_',
})
db.open()

from db.builder_mysql import BuilderMysql


def raw_sql():
    print(db.query('SELECT [[id]], [[username]], [[password]] FROM {{%user}} WHERE [[id]] = :id').bind({':id': 1}).raw_sql())


raw_sql()

item = db.query('SELECT [[id]], [[username]], [[password]] FROM user WHERE [[id]] = :id').bind({':id': 1}).one()
print(item)

# Insert SQL
sql = db.builder().insert('user', {'username': 'sz', 'password': 'pwd'}).raw_sql()
print(sql)
sql = db.builder().insert('user', ['sz', 'pwd']).raw_sql()
print(sql)

# Update SQL
sql = db.builder().update('user', {'username': 'sz', 'password': 'pwd'}, '[[id]]=1').raw_sql()
print(sql)

sql = db.builder().update('user', {'username': 'sz', 'password': 'pwd'}, {'id': 1, 'username': 'sss'}).raw_sql()
print(sql)
