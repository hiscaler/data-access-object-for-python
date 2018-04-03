from db.schema import Schema


class Schema(Schema):
    _table_quote_character = '`'

    _column_quote_character = '`'

    def quote_simple_column_name(self, name):
        return name if name.find("`") > -1 or name == '*' else "`{name}`".format(name=name)
