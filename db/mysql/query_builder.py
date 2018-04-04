# encoding=utf-8
from db.query_builder import QueryBuilder


class QueryBuilder(QueryBuilder):
    def insert(self, table, columns):
        return "INSERT INTO {table} VALUES ()"
