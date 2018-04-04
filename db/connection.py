# encoding=utf-8

"""
see http://kuanghy.github.io/2015/08/16/python-dbapi
"""
from command import Command
from dbexceptions import DatabaseErrorException
from dbexceptions import NotSupportedErrorException
from object import Object


class Connection(Object):
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
        self.table_prefix = ''
        # self.cursor = None

    def connection(self):
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
        self.db = None

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        if self.db is not None:
            return self.db.cursor()
        else:
            raise DatabaseErrorException('No active connection.')

    def create_command(self, sql=None, params={}):
        command = Command(**{'db': self, 'sql': sql})
        if params:
            return command.bind_values(params)
        else:
            return command

    def get_driver_name(self):
        return self._driver

    def get_schema(self):
        if self._schema is not None:
            return self._schema

        driver = self.get_driver_name()
        if driver == 'mysql' or driver == 'pymysql':
            driver = 'mysql'

        if driver in self.schemaMap:
            self._schema = Object.create_object(self.schemaMap[driver], {'db': self})

            print(self._schema)
            return self._schema
        else:
            raise NotSupportedErrorException(
                "Connection does not support reading schema information for '{driver}' DBMS.".format(driver=driver))

    def get_query_builder(self):
        return self.get_schema().get_query_builder()

    def quote_sql(self, sql):
        return sql


if __name__ == '__main__':
    conn = Connection('pymysql', {
        'username': 'root',
        'password': 'root',
        'database': 'dao_test',
        'port': 3306,
        'charset': 'utf-8',
        'table_prefix': '',
    })
    db = conn.connection()
    # Command
    commmand = conn.create_command()
    print(commmand)
    # Query data
    items = conn.create_command('SELECT * FROM user where id = :id', {'id': 1}).query_all()
    print('#' * 80)
    print("Query data result: ")
    print(items)
    print('#' * 80)
    # Insert data
    insert_sql = conn.create_command().insert('user', {'username': 'username1', 'password': '123456'}).get_raw_sql()
    print(insert_sql)
    # print(items)
