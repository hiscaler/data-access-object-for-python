# encoding=utf-8


class Command(object):
    db = None
    params = {}

    def __init__(self):
        self._sql = ''

    def query(self):
        pass

    def query_all(self):
        pass

    def query_one(self):
        pass

    def query_scalar(self):
        pass

    def query_column(self):
        pass

    def insert(self):
        pass

    def batch_insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
