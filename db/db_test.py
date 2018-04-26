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

item = db.query('SELECT [[id]], [[username]], [[password]] FROM user WHERE [[id]] = :id').bind({':id': 2}).one()
print(item)

# Insert SQL
# value is dict
db.builder().insert('user', {'username': 'sz', 'password': 'pwd'}).execute()
# Value is not dict, is list or tuple
db.builder().insert('user', ['sz', 'pwd4444']).execute()

# Update SQL
db.builder().update('user', {'username': 'sz', 'password': 'pwd'}, '[[id]]=1').execute()
db.builder().update('user', {'username': 'sz', 'password': 'pwd'}, {'id': 1, 'username': 'sss'}).execute()

# Delete sql
db.builder().delete('user', {'username': 'sz', 'password': 'pwd'}).execute()
