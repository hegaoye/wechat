# coding=utf-8
import json


class Node:
    def __init__(self):
        self.index = None
        self.text = None
        self.bounds = None
        self.desc = None
        self.package = None
        self.clazz = None

    def get_bounds(self):
        if self.bounds:
            data = str(self.bounds).replace('][', '|').replace('[', '').replace(']', '')
            datas = data.split("|")
            arr1 = str(datas[0]).split(",")
            arr2 = str(datas[1]).split(",")
            x = int(arr1[0]) + (int(arr2[0]) - int(arr1[0])) / 2
            y = int(arr1[1]) + (int(arr2[1]) - int(arr1[1])) / 2
            return [int(x), int(y)]

    def to_json(self):
        '''
        obj to json str
        :return:
        '''
        return json.dumps(self.__dict__)

    def to_obj(self, value):
        '''
        str to obj
        '''
        self.__dict__ = value
        return self
