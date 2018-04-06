# encoding=utf-8


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

    def insert(self, table, columns, params):
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

    def build_condition(self, condition, params):
        return ''

    def build_where(self, condition, params):
        where = self.build_condition(condition, params)

        return 'WHERE ' + where if where != '' else ''

    def update(self, table, columns, condition, params):
        lines = []
        sql = 'UPDATE {table} SET '
        where = ''
        if where:
            sql += ' WHERE ' + where

        return sql
