# coding=utf-8
from src.base.databasetools import Sqlite3Tools


class AccountDao:
    def __init__(self):
        self.db = Sqlite3Tools()

    def load(self, appkey):
        sql = 'select * from user where appkey="' + appkey + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "state": result[4]}
        return None

    def load_by_account_appkey(self, alipay_account, appkey):
        sql = 'select * from user where appkey="' + appkey + '" and account="' + str(alipay_account) + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "state": result[4]}
        return None

    def load_by_account(self, account):
        sql = 'select * from user where account="' + account + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "state": result[4]}
        return None

    def load_by_device_id(self, device_id):
        sql = 'select * from user where device_id="' + str(device_id) + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "state": result[4]}
        return None

    def update(self, account, token):
        """
        更新设备状态
        :param token:登陆后的会话
        """
        sql = 'update account set token="' + str(token) + '"  where account="' + account + '"'
        self.db.update(sql)

    def insert(self, account, appkey, token, device_id):
        sql = "insert into user('account','appkey','token','device_id','state') " \
              "VALUES ('" + str(account) + "','" + str(appkey) + "','" + str(token) + \
              "','" + str(device_id) + "','Used') "
        self.db.insert(sql)

    def delete(self, account):
        sql = "delete from user where account='" + str(account) + "'"
        self.db.delete(sql)
