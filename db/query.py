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
                sql = sql.replace(key, self.db.quote_value(value))

        return self.db.quote_sql(sql)

    def bind(self, params):
        if len(self.params) == 0:
            self.params = params
        else:
            for key, value in params.items():
                self.params[key] = value

        return self

    def _query_internal(self, method):
        raw_sql = self.raw_sql()
        try:
            cursor = self.db.cursor()
            cursor.execute(raw_sql)
            if method == '':
                method = 'all'
            if method == 'all':
                result = cursor.fetchall()
            elif method == 'one':
                result = cursor.fetchone()

            if result:
                columns = [column[0] for column in cursor.description]
                if method == 'all':
                    for item in result:
                        dict(zip(columns, item))
                elif method == 'one':
                    dict(zip(columns, result))

            cursor.close()
            cursor = None
        except Exception as ex:
            raise Exception(str(ex))

        return result

    def one(self):
        return self._query_internal('one')

    def all(self):
        return self._query_internal('all')
