# -*- coding: utf-8 -*-
import json


class BillListData:
    def __init__(self):
        """
        定义账单列表实体类
        """
        self.user = None,
        self.money = 0,
        self.goods = None,
        self.today = None,
        self.time = None,
        self.click_x_y = None

    def to_json(self):
        '''
        obj to json str
        :return:
        '''
        return json.dumps(self.__dict__)

    def to_obj(self, value):
        '''
        dict to obj
        '''
        self.__dict__ = value
        return self
