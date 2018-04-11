# encoding=utf-8

class Query(object):
    def __init__(self, db, sql):
        self.db = db
        self.sql = sql
        self.raw_sql = ''
        self.params = {}

    def sql(self):
        return self.sql

    @property
    def raw_sql(self):
        sql = self.sql
        if len(self.params):
            for key, value in self.params.items():
                sql = sql.repalce(key, value)

        return sql

    def bind(self, params):
        if len(self.params) == 0:
            self.params = params
        else:
            for key, value in params.items():
                self.params[key] = value

        return self
