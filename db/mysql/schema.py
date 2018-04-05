from db.schema import Schema
from db.mysql.query_builder import QueryBuilder


class Schema(Schema):
    _table_quote_character = '`'

    _column_quote_character = '`'

    def quote_simple_table_name(self, name):
        return name if name.find('`') > -1 else "`{name}`".format(name=name)

    def quote_simple_column_name(self, name):
        return name if name.find("`") > -1 or name == '*' else "`{name}`".format(name=name)

    def create_query_builder(self):
        return QueryBuilder(self.db)
