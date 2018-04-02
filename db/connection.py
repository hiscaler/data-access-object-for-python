# encoding=utf-8

"""
see http://kuanghy.github.io/2015/08/16/python-dbapi
"""
from dbexceptions import DatabaseErrorException


class Connection(object):
    apilevel = '1.0'
    paramstyle = 'named'
    threadsafety = 3
    name = None
    schemaMap = {
        'mysql': 'db/mysql/schema'
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
        self.database = ''
        self.port = 3306
        self.charset = 'utf-8'
        self.table_prefix = ''
        self.cursor = None

    def connection(self):
        if self.db is None:
            if self._driver is not None and self._driver in self._drivers_map:
                driver_class = self._drivers_map[self._driver]
                try:
                    __import__(driver_class, globals=globals())
                    print('Driver class is ' + driver_class)
                    if driver_class == 'pymysql':
                        import pymysql
                        self.db = pymysql.connect(self.host, self.username, self.password, self.database)
                except ImportError as ex:
                    print("Import error, {message}.".format(message=str(ex)))

            else:
                raise DatabaseErrorException(
                    '{driver} is not supported or driver name is error.'.format(driver=self._driver))

        return self.db;

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


if __name__ == '__main__':
    conn = Connection('pymysql', {
        'username': 'root',
        'password': 'root',
        'database': 'dao_test',
        'charset': 'utf-8',
        'table_prefix': '',
    })
    db = conn.connection()
    print(db)
