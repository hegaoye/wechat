class Node:
    def __init__(self):
        self.index = None
        self.text = None
        self.bounds = None
        self.desc = None
        self.package = None
        self.clazz = None

    def to_obj(self, value):
        '''
        str to obj
        '''
        self.__dict__ = value
        return self
