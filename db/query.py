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
        return self.raw_sql

    def bind(self, params):
        if len(self.params) == 0:
            self.params = params
        else:
            for key, value in params.items():
                self.params[key] = value

        return self
