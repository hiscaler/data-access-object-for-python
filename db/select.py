# encoding=utf-8

class Select(object):
    def __init__(self, db):
        self.db = db;
        self._selects = []
        self._distinct = False
        self._from = ''
        self.where = ''
        self.join = []
        self.order_by = ''
        self.group_by = ''
        self.having = ''
        self.union = ''
        self.limit = 10
        self.offset = 0
        self.params = {}

    def select(self, columns):
        self._selects = columns

        return self

    def and_select(self, columns):
        self._selects.append(columns)

        return self

    def distinct(self, v=False):
        self._distinct = v

        return self

    def fm(self, tables):
        self._from = tables

        return self

    def where(self, where):
        self.where = where

        return self
