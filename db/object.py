# codeing=utf-8
import importlib
import string


class Object(object):
    def __init__(self, params):
        super(Object, self).__init__()
        for k, v in params.items():
            self.__setattr__(k, v)

    def init(self):
        pass

    @staticmethod
    def create_object(module_name, params=[]):
        module = importlib.import_module(module_name)

        return module
