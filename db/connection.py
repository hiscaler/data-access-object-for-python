# encoding=utf-8


class Connection(object):

    schemaMap = {
        'mysql': 'db/mysql/schema'
    }

    def __init__(self, config={}):
        self._db_class = ''
        self._db = None
        dsn = config['dsn'] if 'dsn' in config else None
        username = config['username'] if 'username' in config else ''
        password = config['password'] if 'password' in config else ''
        if dsn is None or not username or not password:
            raise Exception('Error DSN or username or password value.')

        self.dsn = dsn
        self.username = username
        self.password = password
        self.host = '127.0.0.1'
        self.database = ''
        self.port = 3306
        self.charset = 'utf-8'
        self.table_prefix = ''

    def create_db_instance(self):
        pass

    def open(self):
        if self._db is None:
            return self.create_db_instance()

    def close(self):
        self._db = None

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        pass


if __name__ == '__main__':
    db = Connection()
