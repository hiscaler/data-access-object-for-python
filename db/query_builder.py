# encoding=utf-8

from .conditions.hash_condition import HashCondition
from .dbexceptions import IntegrityErrorException
from .object import Object


class QueryBuilder(object):
    PARAM_PREFIX = ':qp'

    condition_builders = {
        'NOT': 'buildNotCondition',
        'AND': 'buildAndCondition',
        'OR': 'buildAndCondition',
        'BETWEEN': 'buildBetweenCondition',
    }

    condition_classes = {}

    def __init__(self, connection):
        self.db = connection
        self.separator = ' '
        self.type_map = {}

    def insert(self, table, columns):
        if not table or not columns:
            raise IntegrityErrorException("`table` and `rows` param value can't empty.")

        is_dict = isinstance(columns[0], dict)
        schema = self.db.get_schema()
        if is_dict:
            names = []
            values = []
            for name, value in columns.items():
                names.add(schema.quote_column_name(name))
                values.append(schema.quote_value(value))
        else:
            # is list or set or tuple
            names = None
            values = list(schema.quote_value(value) for value in columns)

        sql = "INSERT INTO {table}"
        if names is not None:
            sql += '(' + ', '.join(names) + ')'

        sql += ' VALUES (' + ', '.join(values) + ')'

        return sql.format(table=schema.quote_table_name(table))

    def batch_insert(self, table, rows, names=tuple):
        if not table or not rows:
            raise IntegrityErrorException("`table` and `rows` param value can't empty.")

        is_dict = isinstance(rows[0], dict)
        if not names and not is_dict:
            raise IntegrityErrorException("If `fields` param is empty, then rows must be a dict type.")
        else:
            names = tuple(field for field in rows[0])

        schema = self.db.get_schema()
        names = (schema.quote_column_name(name) for name in names)
        if is_dict:
            values = list(', '.join(tuple(schema.quote_value(row[key]) for key in row)) for row in rows)
        else:
            values = list(', '.join(tuple(schema.quote_value(value) for value in row)) for row in rows)

        sql = "INSERT INTO {table}"
        if names:
            sql += '(' + ', '.join(names) + ')'

        sql += ' VALUES ((' + "), (".join(values) + '))'

        return sql.format(table=schema.quote_table_name(table))

    def build_condition(self, condition, params):
        if isinstance(condition, dict):
            if len(condition) == 0:
                return ''

            condition = self.create_condition(condition)

        return str(condition)

    def create_condition(self, condition):
        if not isinstance(condition, dict):
            operator = condition[0]
            del condition[0]
            if operator in self.condition_classes:
                class_name = self.condition_classes[operator]
            else:
                class_name = 'db.conditions.SimpleCondition'

            cls = Object.create_object(class_name)

            return cls.fromDefinition(operator, condition)

        return HashCondition(condition)

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
