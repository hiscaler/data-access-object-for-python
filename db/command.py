# encoding=utf-8
from object import Object


class Command(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    def bind_values(self, params):
        return self

    def query(self):
        pass

    def query_all(self):
        items = []
        cursor = self.db.cursor()
        cursor.execute(self.sql)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            items.append(dict(zip(columns, row)))

        return items

    def query_one(self):
        pass

    def query_scalar(self):
        pass

    def query_column(self):
        pass

    def insert(self):
        pass

    def batch_insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
