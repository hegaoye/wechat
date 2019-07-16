# coding=utf-8
from src.base.databasetools import Sqlite3Tools


class SettingDao:
    def __init__(self):
        self.db = Sqlite3Tools()

    def load(self, key_enum):
        """
        加载设置
        :param key_enum: 枚举键
        :return:
        """
        sql = 'select * from setting where key="' + str(key_enum.value) + '"'
        result = self.db.load(sql)
        if result:
            return {"key": result[0], "v": result[1]}
        return None

    def update(self, key_enum, value):
        """
        更新设置值
        :param key_enum:键枚举
        :param value:值
        """
        sql = 'update setting set v="' + str(value) + '"  where key="' + key_enum.value + '"'
        self.db.update(sql)

    def insert(self, key_enum, value):
        """
        保存订单记录
        :param order_no: 支付订单号
        :param user: 支付者
        :param money: 支付金额
        :param state: 支付状态
        :param md5: md5值
        :param order_time: 交易时间
        :return:
        """
        sql = "insert into setting('key','v') " \
              "VALUES ('" + str(key_enum.value) + "','" + str(value) + "') "
        self.db.insert(sql)
