# encoding=utf-8


class Schema(object):
    TYPE_PK = 'pk'
    TYPE_UPK = 'upk'
    TYPE_CHAR = 'char'

    _table_quote_character = "'"

    _column_quote_character = '"'

    _table_names = set()

    def __init__(self, db):
        self.db = db
        pass

    def quote_value(self, value):
        if not isinstance(value, str):
            return value

        return "'{value}'".format(value=value)

    def quote_simple_table_name(self, name):
        if isinstance(self._table_quote_character, str):
            starting_character = ending_character = self._table_quote_character
        else:
            starting_character = self._table_quote_character[0]
            ending_character = self._table_quote_character[1]

        return name if name.find(starting_character) > -1 else "{staring}{name}{ending}".format(staring=starting_character, name=name, ending=ending_character)

    def quote_simple_column_name(self, name):
        if isinstance(self._column_quote_character, str):
            starting_character = ending_character = self._column_quote_character
        else:
            starting_character = self._column_quote_character[0]
            ending_character = self._column_quote_character[1]

        return name if name == '*' or name.find(starting_character) > -1 else "{staring}{name}{ending}".format(staring=starting_character, name=name, ending=ending_character)

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
