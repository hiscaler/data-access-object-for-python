# encoding=utf-8

class Select(object):
    def __init__(self, db):
        self.db = db
        self._selects = []
        self._distinct = False
        self._from = ''
        self._where = ''
        self._join = []
        self._order_by = ''
        self._group_by = ''
        self._having = ''
        self._union = ''
        self._limit = 10
        self._offset = 0
        self._params = {}

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

    def from_table(self, tables):
        self._from = tables

        return self

    def where(self, where):
        self._where = where

        return self

    def and_where(self, where):
        self._where = self._where + ' AND ' + where

        return self

    def build(self):
        sql = 'SELECT ' + ", ".join(
            [self.db.quote_column_name(column) for column in self._selects]) + " FROM " + self.db.quote_table_name(
            self._from)
        if self._where is not None and len(self._where):
            sql += ' WHERE ' + self._where

        params = {}
        for key, value in self._params.items():
            params[key] = value

        return self.db.query(sql).bind(params)

    def raw_sql(self):
        return self.build().raw_sql()

    def one(self):
        return self.build().one()

    def all(self):
        return self.build().all()

    def scalar(self):
        return self.build().scalar()

    def column(self):
        return self.build.column()
