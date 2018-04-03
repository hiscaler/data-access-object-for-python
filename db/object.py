# codeing=utf-8
import importlib
import string


class Object(object):
    def __init__(self, configs):
        super(Object, self).__init__()
        for k, v in configs.items():
            self.k = v

    def init(self):
        pass

    @staticmethod
    def get_simple_class_name(class_name):
        # return string.capwords(class_name.split('.')[-1])
        return class_name.split('.')[-1]

    @staticmethod
    def create_object(class_name, params=[]):
        # __import__(class_name)
        # class_name = Object.get_simple_class_name(class_name)
        # print(class_name)
        # exit()
        module = importlib.import_module(class_name)

        return module
