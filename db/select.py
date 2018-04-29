# encoding=utf-8

class Select(object):
    def __init__(self, db):
        self.db = db
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
        if isinstance(columns, str):
            self._selects.append(columns)
        elif isinstance(columns, list) or isinstance(columns, tuple):
            self._selects = columns

        return self

    def add_select(self, columns):
        if isinstance(columns, str):
            self._selects.append(columns)
        elif isinstance(columns, list):
            self._selects += columns
        elif isinstance(columns, tuple):
            self._selects += list(columns)

        return self

    def distinct(self, v=False):
        self._distinct = v

        return self

    def fm(self, tables):
        self._from = tables

        return self

    def where(self, where):
        self.where = where

    def build(self):
        sql = 'SELECT ' + ", ".join(
            [self.db.quote_column_name(column) for column in self._selects]) + " FROM " + self.db.quote_table_name(
            self._from)
        if self.where is not None and len(self.where):
            sql += ' WHERE '

        params = {}
        for key, value in self.params.items():
            params[key] = value

        return self.db.query(sql).bind(params)

    def raw_sql(self):
        return self.build().raw_sql()

    def one(self):
        return self.build().one()
