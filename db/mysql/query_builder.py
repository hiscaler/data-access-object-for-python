# encoding=utf-8
from db.query_builder import QueryBuilder


class QueryBuilder(QueryBuilder):
    def build_limit(self, limit, offset):
        sql = ''
        if self.has_limit(limit):
            sql = ' LIMIT ' + limit
            if self.has_offset(offset):
                sql += ' OFFSET ' + offset
        elif self.has_offset(offset):
            sql = " LIMIT {offset}, 18446744073709551615".format(offset=offset)

        return sql

    def has_limit(self, limit):
        return str(limit).isdigit()

    def has_offset(self, offset):
        offset = str(offset)
        return offset.isdigit() and offset != '0'

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
