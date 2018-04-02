# codeing=utf-8


class Object(object):
    def __init__(self, configs):
        super(Object, self).__init__()
        for k, v in configs.items():
            self.k = v
