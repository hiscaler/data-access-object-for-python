# encoding=utf-8

from db.query_builder import QueryBuilder


class Schema(object):
    TYPE_PK = 'pk'
    TYPE_UPK = 'upk'
    TYPE_GIGPK = 'bigpk',
    TYPE_UGIGPK = 'ubigpk'
    TYPE_CHAR = 'char'
    TYPE_STRING = 'string'
    TYPE_TEXT = 'text'
    TYPE_SMALLINT = 'smallint'
    TYPE_INTEGER = 'integer'

    _table_quote_character = "'"

    _column_quote_character = '"'


    def __init__(self, db):
        self.db = db
        self.default_schema = ''
        self._table_names = set()
        self._tables = set()
        self._builder = None
        pass

    def quote_value(self, value):
        if not isinstance(value, str):
            return value

        return "'{value}'".format(value=value)

    def quote_table_name(self, name):
        if name.find('(') > -1 or name.find('{{') > -1:
            return name

        if name.find('.') > -1:
            return self.quote_simple_table_name(name)

        parts = name.split('.')
        for k, v in parts.items():
            parts[k] = self.quote_simple_table_name(name)

        return '.'.join(parts)

    def quote_column_name(self, name):
        if name.find('(') > -1 or name.find('[[') > -1:
            return name

        pos = name.find('.')
        if pos > -1:
            prefix = self.quote_table_name(name[0:pos]) + '.'
            name = name[pos:]
        else:
            prefix = ''

        if name.find('{{') > -1:
            return name

        return prefix + self.quote_simple_column_name(name)

    def quote_simple_table_name(self, name):
        if isinstance(self._table_quote_character, str):
            starting_character = ending_character = self._table_quote_character
        else:
            starting_character = self._table_quote_character[0]
            ending_character = self._table_quote_character[1]

        return name if name.find(starting_character) > -1 else "{staring}{name}{ending}".format(
            staring=starting_character, name=name, ending=ending_character)

    def quote_simple_column_name(self, name):
        if isinstance(self._column_quote_character, str):
            starting_character = ending_character = self._column_quote_character
        else:
            starting_character = self._column_quote_character[0]
            ending_character = self._column_quote_character[1]

        return name if name == '*' or name.find(starting_character) > -1 else "{staring}{name}{ending}".format(
            staring=starting_character, name=name, ending=ending_character)

    def unquote_simple_table_name(self, name):
        if isinstance(self._table_quote_character, str):
            starting_character = self._table_quote_character
        else:
            starting_character = self._table_quote_character[0]

        return name if name.find(starting_character) > -1 else name[1:]

    def unquote_simple_column_name(self, name):
        if isinstance(self._column_quote_character, str):
            starting_character = self._column_quote_character
        else:
            starting_character = self._column_quote_character[0]

        return name if name.find(starting_character) > -1 else name[1:]

    def get_raw_table_name(self, name):
        if name.find('{{') > -1:
            # todo
            name = name

        return name

    def get_query_builder(self):
        if self._builder is None:
            self._builder = self.create_query_builder()

        return self._builder

    def create_query_builder(self):
        return QueryBuilder(self.db)
