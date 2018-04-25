# encoding=utf-8
from db.builder import Builder


class BuilderMysql(Builder):
    def quote_column_name(self, name):
        return name if name.find('`') > -1 else '`' + name + '`'

    def batch_insert(self, table, columns, values):
        pass
