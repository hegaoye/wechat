# -*- coding: utf-8 -*-
import datetime
import os
import re
import time

import pytesseract
from PIL import Image

from src.service.alipay_data_from_xml import AlipayXmlData


class AliPay:
    def image_to_text(self, img_path, lang='eng'):
        src_img = Image.open(img_path)
        re_str = re.compile(' ')
        text = pytesseract.image_to_string(src_img, lang=lang)
        text = text.replace("+", "").replace("-", "").replace(":", "")
        text = re_str.sub('', text)
        return text

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

    def screen_cap(self, file_name):
        """
        截屏，并保存到 指定目录，最后从手机中拉取到本地项目下进行处理
        :param path:
        :return:
        """
        file_name = str(file_name)
        os.system('adb shell screencap -p /sdcard/' + file_name)
        os.system('adb pull /sdcard/' + file_name)

    def crop(self, x1, y1, x2, y2, src_path, out_path):
        """
        大图按照特定区域的数据进行分片
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param path:
        :param out_path:
        :return:
        """
        src_path = str(src_path)
        out_path = str(out_path)
        img = Image.open(src_path)
        region = (x1, y1, x2, y2)
        crop_img = img.crop(region)
        crop_img.save(out_path)
        return out_path

    def back(self):
        """
        返回一步
        :return:
        """
        os.system("adb shell input keyevent 4")

    def refresh_bill_list(self, ms=500):
        """
        下拉刷新页面
        """
        os.system("adb shell input swipe 900 600 900 2300 " + str(ms))
        time.sleep(.1)
        os.system("adb shell input swipe 900 600 900 900 " + str(ms))

    def crop_order_detail(self):
        """
        截屏详情页，并将订单详情页进行分片，精确去除 订单号，支付账户
        支付金额，状态，时间等必要支付信息
        :return:
        """
        datetime_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        src_filename = 'bill_detail_' + datetime_name + '.png'
        self.screen_cap(src_filename)
        order_no_img_path = self.crop(300, 950, 1050, 1010, src_filename, "order_no_" + src_filename)
        order_money_img_path = self.crop(300, 375, 860, 490, src_filename, "order_money_" + src_filename)
        order_state_img_path = self.crop(410, 515, 670, 575, src_filename, "order_state_" + src_filename)
        order_time_img_path = self.crop(670, 840, 1050, 900, src_filename, "order_time_" + src_filename)
        return src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path

    def get_alipay_account(self):
        """
        读取alipay account
        :return: alipay account
        """
        alipayxmldata = AlipayXmlData()
        if alipayxmldata.is_user_center_page():
            # 从我的页面进入到个人信息页面 点击坐标 850,320
            self.click(850, 320)
            time.sleep(.5)
            alipay_account = alipayxmldata.get_alipay_account()
            self.back()
            if alipay_account:
                return alipay_account
            else:
                return None

    def jump_to_my_page(self):
        alipayxmldata = AlipayXmlData()
        is_user_center_page = alipayxmldata.find_page_keywords("我的", 1)
        if is_user_center_page:
            # 点击我的菜单页进入我的页面
            self.click(980, 2240)
            time.sleep(.5)
            if alipayxmldata.is_user_center_page():
                return True
            else:
                return False
        else:
            self.back()
            time.sleep(.5)
            self.jump_to_my_page()

    def run_xml(self):
        # 1.点击账单
        self.jump_to_my_page()
        alipayxmldata = AlipayXmlData()
        x, y = alipayxmldata.get_bill_click_x_y()
        self.click(x, y)
        # 列表间距查295 px
        for i in range(5):
            self.click(810, 500 + 295 * i)
            time.sleep(.5)
            alipayxmldata.detail()
            self.back()
            time.sleep(0.5)

    def run(self):
        # 1.点击账单
        # self.click(600, 1300)
        time.sleep(0.5)
        # 2.下拉刷新尝试
        self.refresh_bill_list(100)
        time.sleep(0.5)
        # 列表间距查295 px
        self.click(810, 500)
        time.sleep(1)
        src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path = self.crop_order_detail()
        self.back()
        order_no = self.image_to_text(order_no_img_path)
        order_money = self.image_to_text(order_money_img_path)
        order_state = self.image_to_text(order_state_img_path, "chi_sim")
        order_time = self.image_to_text(order_time_img_path)
        print(order_no, order_money, order_state, order_time)
        time.sleep(.5)

        self.click(810, 790)
        time.sleep(1)
        src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path = self.crop_order_detail()
        self.back()
        order_no = self.image_to_text(order_no_img_path)
        order_money = self.image_to_text(order_money_img_path)
        order_state = self.image_to_text(order_state_img_path, "chi_sim")
        order_time = self.image_to_text(order_time_img_path)
        print(order_no, order_money, order_state, order_time)
        time.sleep(.5)

        self.click(810, 1085)
        time.sleep(1)
        src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path = self.crop_order_detail()
        self.back()
        order_no = self.image_to_text(order_no_img_path)
        order_money = self.image_to_text(order_money_img_path)
        order_state = self.image_to_text(order_state_img_path, "chi_sim")
        order_time = self.image_to_text(order_time_img_path)
        print(order_no, order_money, order_state, order_time)
        time.sleep(.5)

        self.click(810, 1380)
        time.sleep(1)
        src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path = self.crop_order_detail()
        self.back()
        order_no = self.image_to_text(order_no_img_path)
        order_money = self.image_to_text(order_money_img_path)
        order_state = self.image_to_text(order_state_img_path, "chi_sim")
        order_time = self.image_to_text(order_time_img_path)
        print(order_no, order_money, order_state, order_time)


if __name__ == "__main__":
    pay_ali = AliPay()
    # pay_ali.run()
    pay_ali.run_xml()
    # print(pay_ali.get_alipay_account())
    # pay_ali.jump_to_my_page()
