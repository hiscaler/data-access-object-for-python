# encoding=utf-8
from object import Object


class Command(object):
    _sql = ''

    raw_sql = ''

    # @var Connection
    db = None

    params = {}

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    def bind_values(self, values):
        if values:
            schema = self.db.get_schema()
            for name, value in values.items():
                if isinstance(name, int):
                    value = str(value)
                self.params[':' + name] = value

        return self

    def query(self):
        pass

    def query_all(self):
        items = []
        raw_sql = self.sql
        for key, value in self.params.items():
            raw_sql = raw_sql.replace(key, str(value))

        self.raw_sql = raw_sql
        cursor = self.db.cursor()
        cursor.execute(self.raw_sql)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            items.append(dict(zip(columns, row)))

        return items

    def query_one(self):
        cursor = self.db.cursor()
        cursor.execute(self.sql)
        columns = [column for column in cursor.description]
        item = cursor.fetchone()
        if item is not None:
            item = dict(zip(columns, item))

        return item

    def query_scalar(self):
        pass

    def query_column(self):
        pass

    def insert(self, table, columns):
        params = {}
        sql = self.db.get_query_builder().insert(table, columns)
        return self.set_sql(sql).bind_values(params)

    def batch_insert(self, table, columns):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def set_sql(self, sql):
        if sql != self._sql:
            self._sql = self.db.quote_sql(sql)
            self.params = {}

        return self

    def get_raw_sql(self):
        if not self.params:
            return self._sql

        params = {}
        for name, value in self.params.items():
            if isinstance(name, str) and name[0:1] != ':':
                name = ':' + name

            if isinstance(value, str):
                params[name] = self.db.quote_value(value)
            elif isinstance(value, bool):
                params[name] = 'TRUE' if value else 'FALSE'
            elif value is None:
                params[name] = 'NULL'
            elif isinstance(value, object):
                params[name] = str(value)

        if 1 not in params:
            sql = self._sql
            for k, v in params.items():
                sql = sql.replace(k, v)
            return sql

        sql = ''
        for i, part in self._sql.split('?').items():
            sql += params[i] if i in params else ''
            sql += part

        return sql
