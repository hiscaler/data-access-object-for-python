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

    def _parse_where(self, where, params={}, operation='AND', append=True):
        """Parse where conditions
        
        @:param where string|dict
        @:param params dict
        @:param operation string
        @:param append boolean
        @:return string
        """
        w = ''
        if isinstance(where, str):
            w = where
            if params is not None and not isinstance(params, dict) and len(params) == 0:
                raise Exception('params type is not dict or is empty.')

            for key, value in params.items():
                w = w.replace(key, self.db.quote_value(value))
        elif isinstance(where, dict):
            for key, value in where.items():
                self._params[':' + key] = value
        else:
            raise Exception('Params error.')

        if len(w) > 0:
            if append:
                if len(self._where) == 0:
                    self._where = w
                else:
                    self._where += ' {op} ({where})'.format(op=operation, where=w)
            else:
                self._where = w

    def where(self, where, params={}):
        self._parse_where(where, params, None, False)

        return self

    def and_where(self, where, params={}):
        self._parse_where(where, params, 'AND')

        return self

    def or_where(self, where, params={}):
        self._parse_where(where, params, 'OR')

        return self

    def build(self):
        sql = 'SELECT ' + ", ".join(
            [self.db.quote_column_name(column) for column in self._selects]) + " FROM " + self.db.quote_table_name(
            self._from)
        if len(self._where):
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
