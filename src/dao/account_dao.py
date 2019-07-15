# coding=utf-8
from src.base.databasetools import Sqlite3Tools


class AccountDao:
    def __init__(self):
        self.db = Sqlite3Tools()

    def load(self, appkey):
        db = Sqlite3Tools()
        sql = 'select * from user where appkey="' + appkey + '"'
        return db.load(sql)

    def update(self, account, token):
        """
        更新设备状态
        :param token:登陆后的会话
        """
        sql = 'update account set token="' + str(token) + '"  where account="' + account + '"'
        self.db.update(sql)

    def insert(self, account, appkey, token):
        """
        保存账户信息
        :param account: 用户名
        :param password: 密码，一般是客户端密码不可修改不共用
        """
        sql = "insert into user('account','appkey','token') " \
              "VALUES ('" + str(account) + "','" + str(appkey) + "','" + str(token) + "') "
        self.db.insert(sql)
