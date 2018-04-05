# encoding=utf-8

from db.dbexceptions import DatabaseErrorException
from db.dbexceptions import NotSupportedErrorException
from db.query_builder import QueryBuilder


class Schema(object):
    TYPE_PK = 'pk'
    TYPE_UPK = 'upk'
    TYPE_BIGPK = 'bigpk'
    TYPE_UBIGPK = 'ubigpk'
    TYPE_CHAR = 'char'
    TYPE_STRING = 'string'
    TYPE_TEXT = 'text'
    TYPE_SMALLINT = 'smallint'
    TYPE_INTEGER = 'integer'
    TYPE_BIGINT = 'bigint'
    TYPE_FLOAT = 'float'
    TYPE_DOUBLE = 'double'
    TYPE_DECIMAL = 'decimal'
    TYPE_DATETIME = 'datetime'
    TYPE_TIMESTAMP = 'timestamp'
    TYPE_TIME = 'time'
    TYPE_DATE = 'date'
    TYPE_BINARY = 'binary'
    TYPE_BOOLEAN = 'boolean'
    TYPE_MONEY = 'money'

    _table_quote_character = "'"

    _column_quote_character = '"'

    def __init__(self, db):
        self.db = db
        self.default_schema = ''
        self._table_names = set()
        self._schema_names = None
        self._tables = {}
        self._builder = None
        pass

    def load_table_schema(self, name):
        pass

    def get_table_schema(self, name, refresh=False):
        if name in self._tables and not refresh:
            return self._tables[name]

        db = self.db
        real_name = self.get_raw_table_name(name)
        self._tables[name] = self.load_table_schema(real_name)

        return self._tables[name]

    def get_table_schemas(self, schema='', refresh=False):
        tables = set()
        for name in self.get_table_names(schema, refresh):
            if schema != '':
                name = schema + '.' + name
            table = self.get_table_schema(name, refresh)
            if table is not None:
                tables.add(table)

        return tables

    def get_schema_names(self, refresh=False):
        if self._schema_names is None or refresh:
            self._schema_names = self.find_schema_names()

        return self._schema_names

    def get_table_names(self, schema, refresh=False):
        if schema not in self._table_names or refresh:
            self._table_names[schema] = self.find_table_names(schema)

        return self._table_names[schema]

    def get_query_builder(self):
        if self._builder is None:
            self._builder = self.create_query_builder()

        return self._builder

    def get_type(self, data):
        pass

    def refresh(self):
        pass

    def create_query_builder(self):
        return QueryBuilder(self.db)

    def find_schema_names(self):
        raise NotSupportedErrorException(self.__class__.__name__ + ' does not support fetching all schema names.')

    def find_table_names(self):
        raise NotSupportedErrorException(self.__class__.__name__ + ' does not support fetching all table names.')

    def get_last_insert_id(self, sequence_name=''):
        if self.db.is_active:
            return self.db.cursor.last_insert_id(None if sequence_name == '' else self.quote_table_name(sequence_name))
        else:
            raise DatabaseErrorException('DB Connection is not active.')

    def supports_savepoint(self):
        return self.db.enable_savepoint

    def create_savepoint(self, name):
        self.db.create_command('SAVEPOINT' + name).execute()

    def release_savepoint(self, name):
        self.db.create_command('RELEASE SAVEPOINT ' + name).execute()

    def rollback_savepoint(self, name):
        self.db.create_command('ROLLBACK TO SAVEPOINT ' + name).execute()

    def set_transaction_isolation_level(self, level):
        self.db.create_command('SET TRANSACTION ISOLATION LEVEL ' + level).execute()

    def insert(self, table, columns):
        command = self.db.create_command().insert(table, columns)
        if not command.execute():
            return False
        result = {}
        table_schema = self.get_table_schema(table)
        for name in table_schema.primary_key:
            pass

        return result

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
