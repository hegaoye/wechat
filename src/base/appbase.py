# coding=utf-8
from time import sleep

import uiautomator2 as u2


class AppBase:
    """
    app通用的功能的封装
    """

    def __init__(self, ip):
        self.d = u2.connect(ip)

    def ip(self):
        return self.d.wlan_ip

    def window_size(self):
        return self.d.window_size()

    def basic_info(self):
        """
        手机基本信息
        :return:
        """
        return self.d.info

    def device_info(self):
        """
        设备信息
        :return:
        """
        return self.d.device_info

    def serial(self) -> str:
        """
        手机的序列号获取
        :return:
        """
        return str(self.d.serial)

    def screen_on(self):
        """
        点亮屏幕
        :return:
        """
        self.d.screen_on()

    def screen_off(self):
        """
        关闭屏幕
        :return:
        """
        self.d.screen_off()

    def screen_status(self):
        """
        获取屏幕状态
        require Android >= 4.4
        :return:
        """
        return self.d.info.get('screenOn')

    def unlock(self):
        """
        解锁
        :return:
        """
        self.d.unlock()

    def home(self):
        """
        返回桌面
        :return:
        """
        self.d.press("home")
        sleep(.5)

    def back(self):
        """
        返回上一步
        :return:
        """
        self.d.press("back")
        sleep(.5)
