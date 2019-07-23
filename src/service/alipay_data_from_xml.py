# coding=utf-8
import datetime
import os

from src.base.xml_path_enum import XMLPath
from src.service.node import Node
from src.service.parse_xml import load_xml, list_attr_value, load_detail_xml


class AlipayXmlData:
    def __init__(self):
        self.abs_alipay_app_path = XMLPath.ABS_ALIPAY_APP_PATH.value
        self.abs_alipay_notify_path = XMLPath.ABS_ALIPAY_NOTIFY_PATH.value
        self.abs_detail_path = XMLPath.ABS_DETAIL_PATH.value
        self.abs_my_path = XMLPath.ABS_MY_PATH.value
        self.abs_personal_path = XMLPath.ABS_PERSONAL_PATH.value
        self.abs_x_path = XMLPath.ABS_X_PATH.value
        self.abs_bill_coordinate_path = XMLPath.ABS_BILL_COORDINATE_PATH.value
        self.abs_bill_path = XMLPath.ABS_BILL_PATH.value
        self.abs_connect_path = XMLPath.ABS_CONNECT_PATH.value

    def __dump_connect_xml(self, device_id):
        """
        是否连接成功设备
        """
        os.system("rm -f " + self.abs_connect_path.replace("{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_CONNECT_PATH.value)
        os.system(
            "adb -s " + str(
                device_id) + " pull " + XMLPath.Sdcard_ABS_CONNECT_PATH.value + " " + self.abs_connect_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_CONNECT_PATH.value)

    def __dump_alipay_notify_xml(self, device_id):
        """
        获取通知栏信息
        """
        os.system("rm -f " + self.abs_alipay_notify_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_ALIPAY_NOTIFY_PATH.value)
        os.system(
            "adb -s " + device_id + " pull  " + XMLPath.Sdcard_ABS_ALIPAY_NOTIFY_PATH.value + "  " + self.abs_alipay_notify_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_ALIPAY_NOTIFY_PATH.value)

    def __dump_alipay_app_xml(self, device_id):
        """
        获取支付宝在桌面的数据文件
        """
        os.system("rm -f " + self.abs_alipay_app_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_ALIPAY_APP_PATH.value)
        os.system(
            "adb -s " + device_id + " pull " + XMLPath.Sdcard_ABS_ALIPAY_APP_PATH.value + "  " + self.abs_alipay_app_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_ALIPAY_APP_PATH.value)

    def __dump_x_page_xml(self, device_id):
        """
        生成判断账单的点击坐标页面
        """
        os.system("rm -f " + self.abs_x_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_X_PATH.value)
        os.system("adb -s " + device_id + " pull " + XMLPath.Sdcard_ABS_X_PATH.value + "  " + self.abs_x_path.replace(
            "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_X_PATH.value)

    def __dump_bill_page_xml(self, device_id):
        """
        生成bill　list　页面
        """
        os.system("rm -f " + self.abs_bill_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_BILL_PATH.value)
        os.system(
            "adb -s " + device_id + " pull  " + XMLPath.Sdcard_ABS_BILL_PATH.value + "  " + self.abs_bill_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_BILL_PATH.value)

    def __dump_personal_page_xml(self, device_id):
        """
        生成个人信息页面用于获取支付宝账户
        :return:
        """
        os.system("rm -f " + self.abs_personal_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_PERSONAL_PATH.value)
        os.system(
            "adb -s " + device_id + " pull  " + XMLPath.Sdcard_ABS_PERSONAL_PATH.value + "  " + self.abs_personal_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_PERSONAL_PATH.value)

    def __dump_my_page_xml(self, device_id):
        """
        导出我的页ui xml
        """
        os.system("rm -f " + self.abs_my_path.replace("{device_id}", device_id))
        os.system("adb -s  " + str(device_id) + "  shell uiautomator dump  " + XMLPath.Sdcard_ABS_MY_PATH.value)
        os.system("adb -s  " + str(
            device_id) + " pull  " + XMLPath.Sdcard_ABS_MY_PATH.value + "  " + self.abs_my_path.replace("{device_id}",
                                                                                                        device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_MY_PATH.value)

    def __dump_bill_coordinate_page_xml(self, device_id):
        """
        导出我的页面并仅提供给提取 账单的坐标提取使用 xml
        """
        os.system("rm -f " + self.abs_bill_coordinate_path.replace("{device_id}", device_id))
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_BILL_COORDINATE_PATH.value)
        os.system(
            "adb -s " + device_id + " pull  " + XMLPath.Sdcard_ABS_BILL_COORDINATE_PATH.value + "  " + self.abs_bill_coordinate_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_BILL_COORDINATE_PATH.value)

    def __dump_detail_xml(self, device_id):
        """
        导出详情页xml
        1.1.导出detail页面的xml数据，必须保障当前屏幕停留在详情页
        2.下载xml到本地
        """
        # 清理数据
        os.system("rm -f " + self.abs_detail_path.replace("{device_id}", device_id))
        # 1.导出detail页面的xml数据，必须保障当前屏幕停留在详情页
        os.system("adb -s " + device_id + " shell uiautomator dump  " + XMLPath.Sdcard_ABS_DETAIL_PATH.value)
        # 2.下载xml到本地
        os.system(
            "adb  -s " + device_id + " pull  " + XMLPath.Sdcard_ABS_DETAIL_PATH.value + "  " + self.abs_detail_path.replace(
                "{device_id}", device_id))
        os.system("adb -s " + str(device_id) + " shell rm -f " + XMLPath.Sdcard_ABS_DETAIL_PATH.value)

    def find_alipay_x_y(self, device_id):
        """
        查找支付宝的 x y 的位置
        :return: x y
        """
        self.__dump_alipay_app_xml(device_id)
        # path device_id
        path = self.abs_alipay_app_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.find("支付宝") >= 0:
                return node.get_bounds()

    def detect_connect(self, device_id):
        """
        检测设备连接是否成功
        :return: 通知总数
        """
        self.__dump_connect_xml(device_id)
        path = self.abs_connect_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        if result_list.__len__() > 0:
            for result in result_list:
                if str(Node().to_obj(result).text).find("充电") > 0:
                    x, y = Node().to_obj(result).get_bounds()
                    return True, x, y

            return False, 0, 0
        else:
            return False, 0, 0

    def notify_list(self, device_id):
        """
        统计支付宝支付通知条数
        :return: 通知总数
        """
        self.__dump_alipay_notify_xml(device_id)
        path = self.abs_alipay_notify_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        count = 0
        if result_list.__len__() > 0:
            for result in result_list:
                if str(Node().to_obj(result).text).find("支付宝") >= 0:
                    count += 1
        return count

    def get_click_clear_notify_x_y(self, device_id):
        """
        找到清理通知的坐标
        :return: x,y
        """
        path = self.abs_alipay_notify_path.replace("{device_id}", device_id)
        result_list = list_attr_value(path, "content-desc", "清")
        # result_list = list_attr_value(path, "resource-id", "com.android.systemui:id/delete")
        if result_list.__len__() > 0:
            return Node().to_obj(result_list[0]).get_bounds()

    def detail(self, device_id):
        """
        转换xml数据，并提取关键数据，返回json格式数据
        :return: json格式数据
        """
        self.__dump_detail_xml(device_id)
        path = self.abs_detail_path.replace("{device_id}", device_id)
        result_list = load_detail_xml(path)
        if result_list.__len__() > 16:
            data = {
                "user": Node().to_obj(result_list[4]).text,
                "orderNo": Node().to_obj(result_list[16]).text,
                "money": Node().to_obj(result_list[5]).text.replace("+", ""),
                "state": Node().to_obj(result_list[6]).text,
                "time": Node().to_obj(result_list[14]).text
            }
            return data

    def get_alipay_account(self, device_id):
        """
        找到用户账户账户
        :return: 账户
        """
        self.__dump_x_page_xml(device_id)
        path = self.abs_x_path.replace("{device_id}", device_id)
        result_list = list_attr_value(path, "resource-id",
                                      "com.alipay.mobile.antui:id/list_right_text")
        if result_list.__len__() == 3:
            return Node().to_obj(result_list[1]).text, Node().to_obj(result_list[0]).text, Node().to_obj(
                result_list[2]).text

    def get_personal_x_y(self, device_id):
        self.__dump_x_page_xml(device_id)
        path = self.abs_x_path.replace("{device_id}", device_id)
        result_list = list_attr_value(path, "resource-id",
                                      "com.alipay.android.phone.wealth.home:id/user_account")
        if result_list.__len__() > 0:
            return Node().to_obj(result_list[0]).get_bounds()

    def find_page_keywords(self, device_id, keyworkds, frequency=1):
        """
        根据支付宝页面的关键词进行检查当前是否在当前页，关键词比如 “我的” 是
        我的页面的关键词，出现2次，频率为2次匹配才算在指定页面，默认最少1次
        :param keyworkds: 关键词，一般为页面独一为二的关键词
        :param frequency: 出现在特殊页面的频次
        :return: True/False
        """
        self.__dump_x_page_xml(device_id)
        path = self.abs_x_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        count = 0
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.__eq__(keyworkds):
                count += 1
        if count >= frequency:
            return True
        else:
            return False

    def find_my_page(self, device_id):
        """
        :param keyworkds: 关键词，一般为页面独一为二的关键词
        :param frequency: 出现在特殊页面的频次
        :return: True/False
        """
        self.__dump_x_page_xml(device_id)
        path = self.abs_x_path.replace("{device_id}", device_id)
        result_list = list_attr_value(path, "resource-id",
                                      "com.alipay.android.phone.wealth.home:id/tab_description")
        if result_list.__len__() > 0:
            x, y = Node().to_obj(result_list[0]).get_bounds()
            return True, x, y
        else:
            return False, 0, 0

    def is_personal_apge(self, device_id):
        """
        是否是个人页面
        :return:True/False
        """
        self.__dump_personal_page_xml(device_id)
        is_personal = False
        is_personal_page = False
        path = self.abs_personal_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.__eq__("个人信息"):
                is_personal = True
            if node.text.__eq__("个人主页"):
                is_personal_page = True

        if is_personal and is_personal_page:
            return True
        else:
            return False

    def is_user_center_page(self, device_id):
        """
        判断当前支付宝所在页面是否是 "我的" 页面
        :return:True/False
        """
        self.__dump_my_page_xml(device_id)
        is_my = False
        is_bill = False
        path = self.abs_my_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.__eq__("我的"):
                is_my = True
            if node.text.__eq__("账单"):
                is_bill = True

        if is_my and is_bill:
            return True
        else:
            return False

    def is_bill_list_page(self, device_id):
        """
        判断当前支付宝所在页面是否是 "账单" 页面
        :return:True/False
        """
        self.__dump_bill_page_xml(device_id)
        count_bill = 0
        path = self.abs_bill_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.__eq__("账单"):
                count_bill += 1

        if count_bill >= 2:
            return True
        else:
            return False

    def get_bill_click_x_y(self, device_id):
        """
        获取 账单的点击坐标 x y
        :return:
        """
        if self.is_user_center_page(device_id):
            self.__dump_bill_coordinate_page_xml(device_id)
            path = self.abs_bill_coordinate_path.replace("{device_id}", device_id)
            result_list = load_xml(path)
            for result in result_list:
                node = Node().to_obj(result)
                if node.text.__eq__("账单"):
                    return node.get_bounds()
        else:
            return False

    def income_list(self, device_id, num):
        """
        获取收入的列表
        :param num:　读取多少条默认５条
        :return: list
        """
        self.__dump_bill_page_xml(device_id)
        path = self.abs_bill_path.replace("{device_id}", device_id)
        result_list = load_xml(path)
        income_list = list()
        for income in result_list:
            data = {
                "user": None,
                "money": 0,
                "goods": None,
                "today": None,
                "time": None,
                "click_x_y": None
            }
            node = Node().to_obj(income)
            if node.text.find("收钱码收款") >= 0 or node.text.find("收款") >= 0:
                index = result_list.index(income)
                for i in range(num):
                    try:
                        node_data = Node().to_obj(result_list[index + i])
                        if i == 0:
                            data["user"] = node_data.text.replace("收钱码收款-来自", "").replace("收款-", "")
                        elif i == 1:
                            money = node_data.text
                            if money.find("-") >= 0:
                                return
                            else:
                                money = money.replace("+", "")
                                data["money"] = float(money)
                            str_data = node_data.bounds
                            str_data = str_data.replace("][", "|").replace("[", "").replace("]", "")
                            str_data_arr = str_data.split("|")
                            arr = str(str_data_arr[1]).split(",")
                            income = int(arr[0])
                            y = int(arr[1]) - 20
                            data["click_x_y"] = [income, y]
                        elif i == 2:
                            data["goods"] = node_data.text
                        elif i == 3:
                            today = node_data.text
                            if today.__eq__("今天"):
                                data["today"] = str(datetime.datetime.now().strftime('%Y%m%d'))
                            elif today.__eq__("昨天"):
                                today = datetime.date.today()
                                oneday = datetime.timedelta(days=1)
                                yesterday = today - oneday
                                data["today"] = str(yesterday)

                        elif i == 4:
                            data["time"] = node_data.text
                    except:
                        pass
                # 不符合数据规范的进行排除
                if not (not data["time"] or not data["today"] or data["click_x_y"][1] < 0):
                    income_list.append(data)

        return income_list
