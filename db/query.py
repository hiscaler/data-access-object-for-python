# encoding=utf-8

class Query(object):
    def __init__(self, db, sql):
        self.db = db
        self.sql = sql
        self.params = {}

    def sql(self):
        return self.sql

    def raw_sql(self):
        sql = self.sql
        if len(self.params):
            for key, value in self.params.items():
                if isinstance(value, int):
                    value = str(value)

                sql = sql.replace(key, value)

        return self.db.quote_sql(sql)

    def bind(self, params):
        if len(self.params) == 0:
            self.params = params
        else:
            for key, value in params.items():
                self.params[key] = value

        return self
