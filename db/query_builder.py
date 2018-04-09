# encoding=utf-8

from db.dbexceptions import IntegrityErrorException


class QueryBuilder(object):
    PARAM_PREFIX = ':qp'

    condition_builders = {
        'NOT': 'buildNotCondition',
        'AND': 'buildAndCondition',
        'OR': 'buildAndCondition',
        'BETWEEN': 'buildBetweenCondition',
    }

    def __init__(self, connection):
        self.db = connection
        self.separator = ' '
        self.type_map = {}

    def insert(self, table, columns):
        schema = self.db.get_schema()
        names = set()
        values = []
        for name, value in columns.items():
            names.add(schema.quote_column_name(name))
            values.append(schema.quote_value(value))

        sql = "INSERT INTO {table}"
        if names:
            sql += '(' + ', '.join(names) + ')'

        sql += ' VALUES (' + ', '.join(values) + ')'

        return sql.format(table=schema.quote_table_name(table))

    def batch_insert(self, table, rows, names=()):
        if not rows:
            raise IntegrityErrorException("`rows` param values can't empty.")

        is_dict = isinstance(rows[0], dict)
        if not names and not is_dict:
            raise IntegrityErrorException("If `fields` param is empty, then rows must be a dict type.")
        else:
            names = set(field for field in rows[0])

        schema = self.db.get_schema()
        names = (schema.quote_column_name(name) for name in names)
        values = []
        if is_dict:
            for row in rows:
                t = []
                for key in row:
                    t.append(schema.quote_value(row[key]))
                values.append(t)
        else:
            for row in rows:
                t = []
                for value in row:
                    t.append(schema.quote_value(value))
                values.append(t)

        sql = "INSERT INTO {table}"
        if names:
            sql += '(' + ', '.join(names) + ')'

        sql += ' VALUES ('
        for value in values:
            sql += '(' + ', '.join(value) + '), '

        sql = sql[0:-2] + ')'

        return sql.format(table=schema.quote_table_name(table))

    def build_condition(self, condition, params):
        return ''

    def build_where(self, condition, params):
        where = self.build_condition(condition, params)

        return 'WHERE ' + where if where != '' else ''

    def update(self, table, columns, condition, params):
        lines = []
        sql = 'UPDATE {table} SET '
        where = self.build_where(condition, params)
        if where:
            sql += ' WHERE ' + where

        return sql.format(table=self.db.quote_table_name(table))

    def delete(self, table, condition, params):
        sql = 'DELETE FROM {table}'
        where = self.build_where(condition, params)
        if where:
            sql += ' WHERE ' + where

        return sql.format(table=self.db.quote_table_name(table))

    def has_limit(self, limit):
        limit = str(limit)
        return limit.isdigit()

    def has_offset(self, offset):
        offset = str(offset)
        return offset.isdigit() and offset != '0'
