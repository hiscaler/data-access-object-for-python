# encoding=utf-8

from .condition import Condition


class HashCondition(Condition):
    def __init__(self, hash):
        self.hash = hash

    def from_definition(self, operator, operands):
        return self(operands)
