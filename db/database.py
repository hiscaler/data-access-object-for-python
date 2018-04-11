# encoding=utf-8

"""
see http://kuanghy.github.io/2015/08/16/python-dbapi
"""
import importlib
import re
import string

from command import Command
from dbexceptions import DatabaseErrorException
from dbexceptions import NotSupportedErrorException
from object import Object
from query import Query


class Database(Object):
    debug = False

    _schema = None
    apilevel = '1.0'
    paramstyle = 'named'
    threadsafety = 3
    name = None
    schemaMap = {
        'mysql': 'db.mysql.schema'
    }
    _drivers_map = {
        'pymysql': 'pymysql',
    }

    _builder = None

    builder_map = {
        'mysql': 'db.builder_mysql',
    }

    def __init__(self, driver, config={}):
        self._driver = driver.lower()
        self._db_class = ''
        self.db = None
        dsn = config['dsn'] if 'dsn' in config else None
        username = config['username'] if 'username' in config else ''
        password = config['password'] if 'password' in config else ''
        if not username or not password:
            raise Exception('Error DSN or username or password value.')

        self.dsn = dsn
        self.username = username
        self.password = password
        self.host = '127.0.0.1'
        self.database = config['database']
        self.port = 3306
        self.charset = 'utf-8'
        table_prefix = ''
        if 'table_prefix' in config:
            table_prefix = config['table_prefix']
        self.table_prefix = table_prefix
        # self.cursor = None

    def open(self):
        if self.db is None:
            if self._driver is not None and self._driver in self._drivers_map:
                driver_class = self._drivers_map[self._driver]
                try:
                    __import__(driver_class, globals=globals())
                    if self.debug:
                        print('Driver class is ' + driver_class)
                    if driver_class == 'pymysql':
                        import pymysql
                        self.db = pymysql.connect(host=self.host, user=self.username, password=self.password,
                                                  database=self.database, port=self.port)
                except ImportError as ex:
                    print("Import error, {message}.".format(message=str(ex)))

            else:
                raise DatabaseErrorException(
                    '{driver} is not supported or driver name is error.'.format(driver=self._driver))

        return self.db

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def commit(self):
        if self.db is not None:
            self.db.commit()

    def rollback(self):
        if self.db is not None:
            self.db.rollback()

    def cursor(self):
        if self.db is not None:
            return self.db.cursor()
        else:
            raise DatabaseErrorException('No active connection.')

    def create_command(self, sql=None, params={}):
        kwargs = {'db': self}
        if sql:
            kwargs['_sql'] = sql
        command = Command(**kwargs)
        return command.bind_values(params) if params else command

    def get_driver_name(self):
        return self._driver

    def get_builder(self):
        if self._builder is not None:
            return self._builder

        driver = self.get_driver_name()
        if driver == 'mysql' or driver == 'pymysql':
            driver = 'mysql'

        if driver in self.builder_map:
            module_name = self.builder_map[driver]
            obj = importlib.import_module(module_name)
            name = "Builder" + string.capwords(module_name.split('_')[-1])
            self._builder = getattr(obj, name)({'db': self})

            return self._builder
        else:
            raise NotSupportedErrorException(
                "Connection does not support reading schema information for '{driver}' DBMS.".format(driver=driver))

    def query(self, sql):
        return Query(self, sql)

    def quote_table_name(self, name):
        return self.get_builder().quote_table_name(name)

    def quote_column_name(self, name):
        return self.get_builder().quote_column_name(name)

    def quote_sql(self, sql):
        pattern = re.compile('(\\{\\{(%?[\w\-\. ]+%?)\\}\\}|\\[\\[([\w\-\. ]+)\\]\\])')
        print re.findall(pattern, sql)
        for item in re.findall(pattern, sql):
            if item[2]:
                replace_value = self.get_builder().quote_column_name(item[2])
            else:
                replace_value = self.get_builder().quote_table_name(item[0].replace('%', self.table_prefix))

            sql = sql.replace(item[0], replace_value)

        return sql
