# -*- coding: utf-8 -*-
import os
import time

from src.dao.account_dao import AccountDao
from src.dao.setting_dao import SettingDao
from src.service.alipay_data_from_xml import AlipayXmlData


class AliPay:
    def __init__(self, device_id, debug):
        self.device_id = str(device_id)
        self.setting_dao = SettingDao()
        self.account_dao = AccountDao()
        self.debug = debug
        self.alipayxmldata = AlipayXmlData()

    def detect_all_devices(self):
        """
        获取所有的设备列表
        :return:
        """
        device_list = os.popen("adb devices")
        _list = list()
        for device in device_list:
            device_id = str(device)
            if device_id.find("device\n") >= 0:
                device_id = device_id.replace("\n", "").replace("device", "").strip()
                _list.append(device_id)

        return _list

    def click(self, x, y):
        """
        点击位置，从左上角开始 0,0
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        x1 = str(x)
        y1 = str(y)
        os.system('adb -s ' + self.device_id + ' shell input tap ' + x1 + ' ' + y1)
        time.sleep(.2)

    def swipe(self, x1, y1, x2, y2):
        """
        滑动位置
        """
        x1 = str(x1)
        y1 = str(y1)
        x2 = str(x2)
        y2 = str(y2)
        os.system('adb -s ' + self.device_id + ' shell input swipe ' + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)
        time.sleep(.2)

    def screen_resolution(self):
        """
        获取屏幕的分辨率
        :return:
        """
        list = os.popen("adb -s " + self.device_id + " shell wm size")
        screen_x_y = None
        for i in list:
            screen_str = str(i).replace("\n", "")
            if screen_str.find("Override size") >= 0:
                screen_x_y = screen_str.replace("Override size: ", "").replace("x", ",")
                break

        if screen_x_y:
            return screen_x_y
        else:
            list = os.popen("adb -s " + self.device_id + " shell wm size")
            for i in list:
                screen_str = str(i).replace("\n", "")
                if screen_str.find("Physical size") >= 0:
                    screen_x_y = screen_str.replace("Physical size: ", "").replace("x", ",")
                    return screen_x_y

    def back(self):
        """
        返回一步
        """
        os.system("adb -s " + self.device_id + " shell input keyevent 4")
        time.sleep(.5)

    def back_to_desktop(self):
        """
        回到桌面
        """
        os.system("adb -s " + self.device_id + " shell input keyevent 3")
        time.sleep(.2)

    def open_notify_pannel(self):
        """
        打开通知栏信息
        """
        os.system("adb -s " + self.device_id + " shell cmd statusbar expand-notifications")
        time.sleep(.2)

    def refresh_bill_list(self, x, y):
        """
        下拉刷新页面
        """
        x = str(int(x) / 2)
        y = str(y)
        os.system("adb -s " + self.device_id + " shell input swipe " + x + " 600 " + x + " " + y + " ")
        time.sleep(.5)

    def scroll_down(self, x1, y1, x2, y2):
        """
        向下滑动页面，从上向下滑动是大的坐标变小的过程，左下角为0,0的坐标，因此
        x1=x2,y1>y2 则 从y1的高度向下滑动到y2的高度位置
        """
        os.system(
            "adb -s " + self.device_id + " shell input swipe  " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(
                y2))
        time.sleep(.2)

    def detect_connect(self, device_id):
        """
        检测设备连接是否成功
        :return:  True/False
        """
        is_online = False
        device_list = self.detect_all_devices()
        for device in device_list:
            if str(device_id).__eq__(str(device)):
                is_online = True
                break

        if is_online:
            is_connected, x, y = self.alipayxmldata.detect_connect(device_id)
            if is_connected:
                self.click(x, y)
                time.sleep(.2)

            return True
        else:
            return False

    def detect_alilpay_notify(self, device_id):
        """
        检测是否有alipay的通知，无论什么通知均返回有通知结果
        :return:  True/False
        """
        self.open_notify_pannel()
        time.sleep(.5)
        notify_count = self.alipayxmldata.notify_list(device_id)
        if notify_count > 0:
            # 清理通知
            if not self.debug:
                x, y = self.alipayxmldata.get_click_clear_notify_x_y(self.device_id)
                self.click(x, y)

            self.back_to_desktop()
            time.sleep(.1)
            return True
        else:
            return False

    def open_alipay_app(self, device_id):
        """
        在桌面上寻找alipay的位置，并打开
        """
        account = self.account_dao.load_by_device_id(device_id)
        if account:
            if account["app_x_y"]:
                x_y = str(account["app_x_y"])
                x_y_arr = x_y.split(",")
                x = x_y_arr[0]
                y = x_y_arr[1]
            else:
                x, y = self.alipayxmldata.find_alipay_x_y(device_id)
                self.account_dao.update_app_x_y(device_id, str(x) + "," + str(y))
        else:
            x, y = self.alipayxmldata.find_alipay_x_y(device_id)

        self.click(x, y)
        time.sleep(.2)

    def get_alipay_account(self, device_id):
        """
        读取alipay account
        :return: alipay account
        """
        if self.alipayxmldata.is_user_center_page(device_id):
            x, y = self.alipayxmldata.get_personal_x_y(device_id)
            self.click(x, y)
            time.sleep(.5)
            account, account_name, taobao_account = self.alipayxmldata.get_alipay_account(device_id)
            self.back()
            if account and account_name and taobao_account:
                return account, account_name, taobao_account
            else:
                return None
        else:
            return None

    def is_shop(self):
        """
        是否是商家判断
        :return: 1是，0否
        """
        is_shop = self.alipayxmldata.find_page_keywords(self.device_id, "商家服务")
        if is_shop:
            return 1
        else:
            return 0

    def jump_to_my_page(self):
        """
        进入我的页面
        :return: True/False
        """
        is_find_my_x_y, x, y = self.alipayxmldata.find_my_page(self.device_id)
        if is_find_my_x_y:
            self.click(x, y)
            time.sleep(.5)
            return True
        else:
            self.back()
            return False

    def entry_bill_list_page(self):
        """
        进入到账单列表页面
        """
        is_bill_list_page = self.alipayxmldata.is_bill_list_page(self.device_id)
        if is_bill_list_page:
            account = self.account_dao.load_by_device_id(self.device_id)
            if account and account["screen_x_y"]:
                x_y = str(account["screen_x_y"])
                x_y_arr = x_y.split(",")
                x, y = x_y_arr[0], x_y_arr[1]
                self.refresh_bill_list(x=x, y=y)
                return

            self.refresh_bill_list(x=600, y=2300)
        else:
            is_my_page = self.jump_to_my_page()
            if is_my_page:
                account = self.account_dao.load_by_device_id(self.device_id)
                if account and account["bill_x_y"]:
                    x_y = str(account["bill_x_y"])
                    x_y_arr = x_y.split(",")
                    x, y = x_y_arr[0], x_y_arr[1]
                    self.click(x, y)
                    time.sleep(.5)
                    return

                x, y = self.alipayxmldata.get_bill_click_x_y(self.device_id)
                self.account_dao.update_bill_x_y(self.device_id, str(x) + "," + str(y))
                self.click(x, y)
                time.sleep(.5)
            else:
                self.back()

    def income_list(self, limit=5):
        """
        获取账单页面列表信息
        :return:
        """
        income_list = self.alipayxmldata.income_list(self.device_id, limit)
        return income_list

    def order_detail(self, x, y, is_shop):
        """
        读取订单支付详情信息
        :return:　data
        """
        self.click(x, y)
        time.sleep(.5)
        return self.alipayxmldata.detail(self.device_id, is_shop)
