# coding=utf-8
import datetime

from src.base.databasetools import Sqlite3Tools


class BillDao:
    def __init__(self):
        self.db = Sqlite3Tools()

    def load(self, order_no):
        """
        查询一个订单号
        :param order_no: 订单号
        :return: Bill
        """
        sql = 'select * from bill where order_no="' + order_no + '"'
        return self.db.load(sql)

    def delete_by_time(self, time):
        """
        删除前天的数据避免数据过大
        :param time: 前天时间
        """
        sql = 'delete from bill where create_time<="' + time + '"'
        self.db.delete(sql)

    def insert(self, order_no, user, money, state, md5, order_time, account):
        """
        保存订单记录
        :param order_no: 支付订单号
        :param user: 支付者
        :param money: 支付金额
        :param state: 支付状态
        :param md5: md5值
        :param order_time: 交易时间
        :param account: 支付账户
        """
        sql = 'insert into bill("order_no","account","user","money","state","md5","order_time","create_time") ' \
              ' values("' + str(order_no) + '","' + str(account) + '","' + str(user) + '","' + str(money) + '","' \
              + str(state) + '","' + str(md5) + '","' + str(order_time) + '","' \
              + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '")'
        self.db.insert(sql)
