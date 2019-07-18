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
                    "screen_x_y": result[4], "bill_x_y": result[5], "app_x_y": result[6]}
        return None

    def load_by_account_appkey(self, alipay_account, appkey):
        sql = 'select * from user where appkey="' + appkey + '" and account="' + str(alipay_account) + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "screen_x_y": result[4], "bill_x_y": result[5], "app_x_y": result[6]}
        return None

    def load_by_account(self, account):
        sql = 'select * from user where account="' + account + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "screen_x_y": result[4], "bill_x_y": result[5], "app_x_y": result[6]}
        return None

    def load_by_device_id(self, device_id):
        sql = 'select * from user where device_id="' + str(device_id) + '"'
        result = self.db.load(sql)
        if result:
            return {"account": result[0], "appkey": result[1], "token": result[2], "device_id": result[3],
                    "screen_x_y": result[4], "bill_x_y": result[5], "app_x_y": result[6]}
        return None

    def update(self, account, token):
        """
        更新设备状态
        :param token:登陆后的会话
        """
        sql = 'update user set token="' + str(token) + '"  where account="' + account + '"'
        self.db.update(sql)

    def update_bill_x_y(self, device_id, bill_x_y):
        """
        更新设备 账单的点击x y坐标
        """
        sql = 'update user set bill_x_y="' + str(bill_x_y) + '"  where device_id="' + device_id + '"'
        self.db.update(sql)

    def update_app_x_y(self, device_id, app_x_y):
        """
        更新设备 账单的点击x y坐标
        """
        sql = 'update user set app_x_y="' + str(app_x_y) + '"  where device_id="' + device_id + '"'
        self.db.update(sql)

    def insert(self, account, appkey, token, device_id, screen_x_y):
        """
        保存用户信息，设备信息
        :param account: 用户账户
        :param appkey: appkey
        :param token: 登录token
        :param device_id: 设备编码
        :param screen_x_y: 屏幕的x,y坐标
        """
        sql = "insert into user('account','appkey','token','device_id','screen_x_y') " \
              "VALUES ('" + str(account) + "','" + str(appkey) + "','" + str(token) + \
              "','" + str(device_id) + "','" + str(screen_x_y) + "') "
        self.db.insert(sql)

    def delete(self, device_id):
        """
        根据设备id进行清理
        :param device_id: 设备id
        """
        sql = "delete from user where device_id='" + str(device_id) + "'"
        self.db.delete(sql)
