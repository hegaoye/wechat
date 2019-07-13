# coding=utf-8
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
        db = Sqlite3Tools()
        sql = 'select * from bill where order_no="' + order_no + '"'
        return db.load(sql)

    def queryLogs(self):
        """
        查询日志集合，通过job进行分组
        :return:
        """
        sql = "select * from logs group by job"
        results = self.db.query(sql)
        list = []
        for row in results:
            list.append(
                {'id': row[0], 'code': row[1], 'job': row[2], 'log': row[3], 'account': row[4], 'createTime': row[5]})
        return list

    def queryLogsByJob(self, job=None):
        """
        查询日志集合
        :param job: 执行的预定日志 Auth,Lock,DoorLight,BedLight,RoomLight
        :return:
        """
        sql = "select * from logs where job='" + job + "' order by createTime desc"
        results = self.db.query(sql)
        list = []
        for row in results:
            list.append(
                {'id': row[0], 'code': row[1], 'job': row[2], 'log': row[3], 'account': row[4], 'createTime': row[5]})
        return list

    def insert(self, order_no):
        """
        保存日志信息
        :param logpojo: 日志对象
        """
        sql = "insert into bill('order_no',order_no,'log','account','createTime') " \
              "VALUES ('" + str(logpojo.code) + "','" + str(logpojo.job) + "','" + str(logpojo.log) + "','" + str(
            logpojo.accout) + "','" + logpojo.createTime + "') "
        self.db.insert(sql)
