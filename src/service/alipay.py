# -*- coding: utf-8 -*-
import os
import time

from src.base.command import Command
from src.dao.setting_dao import SettingDao
from src.service.alipay_data_from_xml import AlipayXmlData


class AliPay:
    def __init__(self):
        self.setting_dao = SettingDao()
        self.alipayxmldata = AlipayXmlData()

    def click(self, x, y):
        """
        点击位置，从左上角开始 0,0
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        x1 = str(x)
        y1 = str(y)
        os.system('adb shell input tap ' + x1 + ' ' + y1)
        time.sleep(.2)

    def swipe(self, x1, y1, x2, y2):
        """
        滑动位置
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        x1 = str(x1)
        y1 = str(y1)
        x2 = str(x2)
        y2 = str(y2)
        os.system('adb shell input swipe ' + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)
        time.sleep(.2)

    def back(self):
        """
        返回一步
        """
        os.system("adb shell input keyevent 4")
        time.sleep(.5)

    def back_to_desktop(self):
        """
        回到桌面
        """
        os.system("adb shell input keyevent 3")
        time.sleep(.2)

    def open_notify_pannel(self):
        """
        打开通知栏信息
        """
        os.system("adb shell input swipe 900 0 900 900 100")
        time.sleep(.2)

    def refresh_bill_list(self, ms=500):
        """
        下拉刷新页面
        """
        os.system("adb shell input swipe 900 600 900 2300 " + str(ms))
        time.sleep(.2)

    def scroll_down(self, ms=300):
        """
        向下滑动页面
        :param ms:下滑时间长度
        """
        os.system("adb shell input swipe 900 900 400 400 " + str(ms))
        time.sleep(.2)

    def detect_alilpay_notify(self):
        """
        检测是否有alipay的通知，无论什么通知均返回有通知结果
        :return:  True/False
        """
        self.back_to_desktop()
        time.sleep(.1)
        self.open_notify_pannel()
        time.sleep(.1)
        notify_count = self.alipayxmldata.notify_list()
        # TODO 清理通知
        self.back_to_desktop()
        time.sleep(.1)
        if notify_count > 0:
            return True
        else:
            return False

    def open_alipay_app(self):
        """
        在桌面上寻找alipay的位置，并打开
        """
        app_x_y_setting = self.setting_dao.load(Command.App_x_y)
        if app_x_y_setting:
            x_y = str(app_x_y_setting["v"])
            x_y_arr = x_y.split(",")
            self.click(x_y_arr[0], x_y_arr[1])
        else:
            x, y = self.alipayxmldata.find_alipay_x_y()
            self.setting_dao.insert(Command.App_x_y, str(x) + "," + str(y))
            self.click(x, y)
        time.sleep(.2)

    def get_alipay_account(self):
        """
        读取alipay account
        :return: alipay account
        """
        if self.alipayxmldata.is_user_center_page():
            # 从我的页面进入到个人信息页面 点击坐标 850,320
            self.click(850, 320)
            time.sleep(.5)
            alipay_account = self.alipayxmldata.get_alipay_account()
            self.back()
            if alipay_account:
                return alipay_account
            else:
                return None

    def jump_to_my_page(self):
        is_user_center_page = self.alipayxmldata.find_page_keywords("我的", 1)
        if is_user_center_page:
            # 点击我的菜单页进入我的页面
            self.click(980, 2240)
            time.sleep(.5)
            if self.alipayxmldata.is_user_center_page():
                return True
            else:
                return False
        else:
            self.back()
            self.jump_to_my_page()

    def income_list(self, limit=5, page=2):
        """
        获取账单页面列表信息
        :return:
        """
        bill_x_y_setting = self.setting_dao.load(Command.Bill_x_y)
        if bill_x_y_setting:
            x_y = str(bill_x_y_setting["v"])
            x_y_arr = x_y.split(",")
            self.click(x_y_arr[0], x_y_arr[1])
        else:
            x, y = self.alipayxmldata.get_bill_click_x_y()
            self.setting_dao.insert(Command.Bill_x_y, str(x) + "," + str(y))
            self.click(x, y)

        time.sleep(.5)
        all_list = list()
        for i in range(page):
            income_list = self.alipayxmldata.income_list(limit)
            print(income_list)
            if income_list.__len__() > 0:
                all_list.extend(income_list)
            if page - 1 - i > 0:
                self.scroll_down()
                time.sleep(.5)

        return all_list

    def order_detail(self, x, y):
        """
        读取订单支付详情信息
        :return:　data
        """
        self.click(x, y)
        time.sleep(.5)
        return self.alipayxmldata.detail()


if __name__ == "__main__":
    pay_ali = AliPay()
    # pay_ali.run()
    # pay_ali.run_xml()
    # pay_ali.open_alipay_app()
    # pay_ali.jump_to_my_page()
    # print(pay_ali.income_list(limit=5, page=4))
    # pay_ali.scroll_down()

    flag = pay_ali.detect_alilpay_notify()
    if flag:
        pay_ali.open_alipay_app()
