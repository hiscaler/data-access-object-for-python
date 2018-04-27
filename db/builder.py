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

    def batch_insert(self, table, columns, values):
        """Generate batch INSERT sql"""
        if not isinstance(values, list) and not isinstance(values, tuple):
            raise Exception('values params error.')

        if len(values[0]) != len(columns):
            raise Exception('fields length is not match values')

        params = {}
        rows = []
        for i in range(len(values)):
            row_params = []
            row = values[i]
            for key in range(len(row)):
                k = ':' + str(columns[key]) + str(i) + str(key)
                row_params.append(k)
                params[k] = row[key]
            rows.append('(' + ', '.join(row_params) + ')')

        columns = [self.db.quote_column_name(column) for column in columns]
        sql = "INSERT INTO {table} ({columns}) VALUES {values}".format(table=self.db.quote_table_name(table),
                                                                       columns=', '.join(columns),
                                                                       values=', '.join(rows))

        return self.db.query(sql).bind(params)

    @abstractmethod
    def update(self, table, columns, where=None):
        params = {}
        names = values = lines = []
        for column, value in columns.items():
            name = self.db.quote_column_name(column)
            k = ':' + str(column)
            lines.append(name + " = " + k)
            params[k] = value

        sql = "UPDATE {table} SET {lines}".format(table=self.db.quote_table_name(table), lines=', '.join(lines))
        if where is not None and len(where):
            if isinstance(where, str):
                sql += ' WHERE ' + self.db.quote_sql(where)
            elif isinstance(where, dict):
                s = []
                for column, value in where.items():
                    s.append(self.db.quote_column_name(column) + ' = ::' + column)
                    params['::' + column] = value
                sql += ' WHERE ' + ' AND '.join(s)
            else:
                sql += ' WHERE 0 = 1'

        return self.db.query(sql).bind(params)

    def delete(self, table, where=None):
        """Generate DELETE sql"""
        sql = 'DELETE FROM {table}'.format(table=self.db.quote_table_name(table))
        params = {}
        if where is not None and len(where):
            if isinstance(where, str):
                sql += ' WHERE ' + where
            elif isinstance(where, dict):
                w = []
                for name, value in where.items():
                    w.append(self.db.quote_column_name(name) + ' = :' + name)
                    params[':' + name] = value
                sql += ' WHERE ' + ' AND '.join(w)

        return self.db.query(sql).bind(params)

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
