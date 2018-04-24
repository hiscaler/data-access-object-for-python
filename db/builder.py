# encoding=utf-8
from abc import ABCMeta, abstractmethod


class Builder(object):
    def __init__(self, db):
        self.db = db

    @classmethod
    @abstractmethod
    def one(cls, sql):
        pass

    def insert(self, table, params):
        """Insert data"""
        columns = []
        values = []
        if isinstance(params, dict):
            for name, value in params.items():
                columns.append(self.db.quote_column_name(name))
                k = ':' + name
                values.append(k)
                del params[name]
                params[k] = value
        else:
            _params = {}
            for i, value in enumerate(params):
                k = ':' + str(i)
                values.append(k)
                _params[k] = value
            params = _params

        if len(columns) == 0:
            sql = "INSERT INTO {table} DEFAULT VALUES ({values})".format(table=self.db.quote_table_name(table),
                                                                         values=', '.join(values))
        else:
            sql = "INSERT INTO {table} ({columns}) VALUES ({values})".format(table=self.db.quote_table_name(table),
                                                                             columns=', '.join(columns),
                                                                             values=', '.join(values))

        return self.db.query(sql).bind(params)

    @classmethod
    @abstractmethod
    def update(cls, table, columns, condition):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, table, condition):
        pass

    def truncate_table(self, table):
        sql = 'TRUNCATE TABLE {table}'.format(table=self.db.quote_table_name(table))

        return self.db.query(sql)

    @staticmethod
    def quote(s):
        return "'" + str(s).replace("'", "''") + "'"

    @staticmethod
    def quote_simple_table_name(name):
        return name if name.find('"') > -1 else '"' + name + '"'

    def quote_table_name(self, name):
        return self.quote_simple_table_name(name)

    @staticmethod
    def quote_simple_column_name(name):
        return name if name.find('"') > -1 or name == '*' else '"' + name + '"'

    def quote_column_name(self, name):
        return self.quote_simple_column_name(name)

    def quote_value(self, value):
        return self.quote(value)
