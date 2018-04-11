# conding=utf-8
from database.builder_mysql import MysqlBuilder
query_builder = MysqlBuilder()
sql = query_builder.insert('user', {'username': 'name1'})
print(sql)
