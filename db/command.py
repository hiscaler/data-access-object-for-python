# encoding=utf-8
from object import Object


class Command(object):
    raw_sql = ''
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

    def insert(self):
        pass

    def batch_insert(self, table, columns):
        fields = values = []
        for field, value in columns.items:
            fields.append(field)
            values.append(value)
        sql = "INSERT INTO {table}"

    def update(self):
        pass

    def delete(self):
        pass
