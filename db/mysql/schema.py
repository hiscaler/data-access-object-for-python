from db.schema import Schema


class Schema(Schema):
    def quote_simple_column_name(self, name):
        return name if name.find("`") > -1 or name == '*' else "`{name}`".format(name=name)
