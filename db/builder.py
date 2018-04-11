# encoding=utf-8
from abc import ABCMeta, abstractmethod


class Builder(object):
    def __init__(self, db):
        self.db = db

    @classmethod
    @abstractmethod
    def one(cls, sql):
        pass

    @classmethod
    @abstractmethod
    def insert(cls, table, values):
        pass

    @classmethod
    @abstractmethod
    def update(cls, table, columns, condition):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, table, condition):
        pass

    @staticmethod
    def quote(self, s):
        return "'" + s.replace("'", "''") + "'"

    @staticmethod
    def quote_simple_table_name(self, name):
        return name if name.find('"') > -1 else '"' + name + '"'

    def quote_table_name(self, name):
        return self.quote_simple_table_name(name)

    @staticmethod
    def quote_simple_column_name(self, name):
        return name if name.find('"') > -1 or name == '*' else '"' + name + '"'

    def quote_column_name(self, name):
        return self.quote_simple_column_name(name)

    def quote_value(self, value):
        return self.quote(value)
