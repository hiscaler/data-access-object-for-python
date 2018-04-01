# encoding=utf-8


class Schema(object):
    TYPE_PK = 'pk'
    TYPE_UPK = 'upk'
    TYPE_CHAR = 'char'

    def __init__(self):
        self.db = None

    def quote_value(self, value):
        if not isinstance(value, str):
            return value

        return "'{value}'".format(value=value)

    def quote_simple_table_name(self, name):
        return name if name.find("'") > -1 else "'{name}'".format(name=name)
