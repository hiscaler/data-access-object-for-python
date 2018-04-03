# encoding=utf-8


class QueryBuilder(object):
    PARAM_PREFIX = ':qp'

    condition_builders = {
        'NOT': 'buildNotCondition',
        'AND': 'buildAndCondition',
        'OR': 'buildAndCondition',
        'BETWEEN': 'buildBetweenCondition',
    }

    def __init__(self, connection):
        self.db = connection
        self.separator = ' '
        self.type_map = {}
