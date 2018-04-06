# encoding=utf-8
from object import Object
from db.data_reader import DataReader


class Command(object):
    _sql = ''

    # @var Connection
    db = None

    cursor = None

    fetch_mode = 'assoc'

    params = {}

    _pending_params = {}

    _sql = ''

    def __init__(self, **kwargs):
        # self.cursor = None
        # self.fetch_mode = 'assoc'
        # self.params = {}
        # self._pending_params = {}
        # self._sql = ''

        self._refresh_table_name = None
        for name, value in kwargs.items():
            self.__setattr__(name, value)

        self.cursor = self.db.cursor()
        if self._sql:
            self._sql = self.db.quote_sql(self._sql)

    def get_sql(self):
        return self._sql

    def set_sql(self, sql):
        if sql != self._sql:
            self._sql = self.db.quote_sql(sql)

        return self

    def set_raw_sql(self, sql):
        if sql != self._sql:
            self._sql = sql

        return self

    def get_raw_sql(self):
        if not self.params:
            return self._sql

        params = {}
        for name, value in self.params.items():
            if isinstance(name, str) and name[0:1] != ':':
                name = ':' + name

            if isinstance(value, str):
                params[name] = self.db.get_schema().quote_value(value)
            elif isinstance(value, bool):
                params[name] = 'TRUE' if value else 'FALSE'
            elif value is None:
                params[name] = 'NULL'
            elif isinstance(value, object):
                params[name] = str(value)

        if 1 not in params:
            sql = self._sql
            for k, v in params.items():
                sql = sql.replace(k, v)
            return sql

        sql = ''
        for i, part in self._sql.split('?').items():
            sql += params[i] if i in params else ''
            sql += part

        return sql

    def cancel(self):
        if self.cursor is not None:
            self.cursor.close()

    def bind_param(self, name, value, data_type=None, length=None, driver_options=None):
        pass

    def _bind_pending_params(self):
        pass

    def bind_value(self, name, value, data_type=None):
        if data_type is None:
            data_type = self.db.get_schema().get_type(value)

        self._pending_params[name] = [value, data_type]
        self.params[name] = value

        return self

    def bind_values(self, values):
        if values:
            schema = self.db.get_schema()
            for name, value in values.items():
                if isinstance(value, list) or isinstance(value, set):
                    self._pending_params[name] = value
                    self.params[name] = value[0]
                else:
                    if isinstance(value, int):
                        value = str(value)
                    self._pending_params[name] = (value, schema.get_type(value))
                    self.params[name] = value

        return self

    def query(self):
        return self.query_internal('')

    def query_all(self, fetch_mode=None):
        return self.query_internal('all', fetch_mode)
        items = []
        raw_sql = self.sql
        for key, value in self.params.items():
            raw_sql = raw_sql.replace(key, str(value))

        self.raw_sql = raw_sql
        cursor = self.db.cursor()
        print self.raw_sql
        exit()
        cursor.execute(self.raw_sql)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            items.append(dict(zip(columns, row)))

        return items

    def query_one(self, fetch_mode=None):
        return self.query_internal('one', fetch_mode)
        cursor = self.db.cursor()
        cursor.execute(self.sql)
        columns = [column for column in cursor.description]
        item = cursor.fetchone()
        if item is not None:
            item = dict(zip(columns, item))

        return item

    def query_scalar(self, fetch_mode):
        result = self.query_internal('one', fetch_mode)

        return result

    def query_column(self, fetch_mode):
        result = self.query_internal('all', fetch_mode)

    def insert(self, table, columns):
        params = {}
        sql = self.db.get_query_builder().insert(table, columns)

        return self.set_sql(sql).bind_values(params)

    def batch_insert(self, table, columns, rows):
        sql = self.db.get_query_builder().batch_insert(table, columns, rows)

        return self.set_sql(sql)

    def update(self, table, columns, condition='', params={}):
        sql = self.db.get_query_builder().update(table, columns, condition, params)

        return self.set_sql(sql).bind_values(params)

    def delete(self, table, condition='', params={}):
        sql = self.db.get_query_builder().delete(table, condition, params)

        return self.set_sql(sql).bind_values(params)

    def execute(self):
        sql = self.get_sql()
        if sql == '':
            return 0

        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.rowcount
        except Exception as ex:
            self.db.rollback()
            raise Exception(
                "Execute `{sql}` sql error, error message: {message}".format(sql=self.get_raw_sql(), message=str(ex)))

    def query_internal(self, method, fetch_mode=None):
        raw_sql = self.get_raw_sql()
        try:
            self.cursor.execute(raw_sql)
            if method == '':
                method = 'all'
            if method == 'all':
                result = self.cursor.fetchall()
            elif method == 'one':
                result = self.cursor.fetchone()

            if result is not None:
                columns = [column[0] for column in self.cursor.description]
                result = dict(zip(columns, result))

            self.cursor.close()
            self.cursor = None
        except Exception as ex:
            print raw_sql
            raise Exception(str(ex))

        return result

    def require_table_schema_refresh(self, name):
        self._refresh_table_name = name

        return self

    def refresh_table_schema(self):
        if self._refresh_table_name is not None:
            self.db.get_schema().refresh_table_schema(self._refresh_table_name)
