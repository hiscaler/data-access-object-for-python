# encoding=utf-8


class Connection(object):
    schemaMap = {
        'mysql': 'db/mysql/schema'
    }

    def __init__(self):
        self._db = None
        self.dsn = None
        self.username = ''
        self.password = ''
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
