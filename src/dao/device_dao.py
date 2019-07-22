# coding=utf-8

from src.base.databasetools import Sqlite3Tools


class DeviceDao:
    def __init__(self):
        self.db = Sqlite3Tools()

    def load(self, device_id):
        """
        查询一个设备
        :param device_id: 设备id
        :return: 设备
        """
        sql = 'select * from devices where device_id="' + str(device_id) + '"'
        return self.db.load(sql)

    def loadone(self):
        """
        查询一个设备
        :param device_id: 设备id
        :return: 设备
        """
        sql = 'select * from devices where state="Free" limit 1'
        result = self.db.load(sql)
        if result:
            return result[0]
        else:
            return None

    def delete_by_id(self, device_id):
        """
        删除掉线的设备
        :param date_time: 过期时间
        """
        sql = 'delete from devices where device_id=="' + str(device_id) + '"'
        self.db.delete(sql)

    def delete(self):
        """
        删除掉线的设备
        :param date_time: 过期时间
        """
        sql = 'delete from devices'
        self.db.delete(sql)

    def update(self, device_id):
        """
        更新设备 账单的点击x y坐标
        """
        sql = 'update devices set state="Used" where device_id="' + device_id + '"'
        self.db.update(sql)

    def insert(self, device_id):
        """
        保存设备记录
        :param device_id: 设备id
        """
        sql = 'insert into devices("device_id","state") ' \
              ' values("' + str(device_id) + '","Free")'
        self.db.insert(sql)
