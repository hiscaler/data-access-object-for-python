# encoding=utf-8
from .condition import Condition


class AndCondition(Condition):
    def get_operator(self):
        return 'AND'
