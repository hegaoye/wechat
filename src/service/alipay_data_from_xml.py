import datetime
import os

from src.service.node import Node
from src.service.parse_xml import load_xml


class AlipayXmlData:
    def __init__(self):
        self.abs_alipay_app_path = "/home/scrapy_pay_client/alipay_app.xml"
        self.abs_alipay_notify_path = "/home/scrapy_pay_client/notify.xml"
        self.abs_detail_path = "/home/scrapy_pay_client/bill_detail.xml"
        self.abs_my_path = "/home/scrapy_pay_client/my_page.xml"
        self.abs_personal_path = "/home/scrapy_pay_client/personal_page.xml"
        self.abs_x_path = "/home/scrapy_pay_client/x_page.xml"
        self.abs_bill_coordinate_path = "/home/scrapy_pay_client/bill_coordinate_page.xml"
        self.abs_bill_path = "/home/scrapy_pay_client/bill_list_page.xml"

    def __dump_alipay_notify_xml(self):
        """
        获取通知栏信息
        """
        os.system("rm -f " + self.abs_alipay_notify_path)
        os.system("adb shell uiautomator dump /sdcard/notify.xml")
        os.system("adb pull /sdcard/notify.xml " + self.abs_alipay_notify_path)

    def __dump_alipay_app_xml(self):
        """
        获取支付宝在桌面的数据文件
        """
        os.system("rm -f " + self.abs_alipay_app_path)
        os.system("adb shell uiautomator dump /sdcard/alipay_app.xml")
        os.system("adb pull /sdcard/alipay_app.xml " + self.abs_alipay_app_path)

    def __dump_x_page_xml(self):
        """
        生成判断账单的点击坐标页面
        """
        os.system("rm -f " + self.abs_x_path)
        os.system("adb shell uiautomator dump /sdcard/x.xml")
        os.system("adb pull /sdcard/x.xml " + self.abs_x_path)

    def __dump_bill_page_xml(self):
        """
        生成bill　list　页面
        """
        os.system("rm -f " + self.abs_bill_path)
        os.system("adb shell uiautomator dump /sdcard/bill_list_page.xml")
        os.system("adb pull /sdcard/bill_list_page.xml " + self.abs_bill_path)

    def __dump_personal_page_xml(self):
        """
        生成个人信息页面用于获取支付宝账户
        :return:
        """
        os.system("rm -f " + self.abs_personal_path)
        os.system("adb shell uiautomator dump /sdcard/personal_page.xml")
        os.system("adb pull /sdcard/personal_page.xml " + self.abs_personal_path)

    def __dump_my_page_xml(self):
        """
        导出我的页ui xml
        """
        os.system("rm -f " + self.abs_my_path)
        os.system("adb shell uiautomator dump /sdcard/my_page.xml")
        os.system("adb pull /sdcard/my_page.xml " + self.abs_my_path)

    def __dump_bill_coordinate_page_xml(self):
        """
        导出我的页面并仅提供给提取 账单的坐标提取使用 xml
        """
        os.system("rm -f " + self.abs_bill_coordinate_path)
        os.system("adb shell uiautomator dump /sdcard/bill_coordinate_page.xml")
        os.system("adb pull /sdcard/bill_coordinate_page.xml " + self.abs_bill_coordinate_path)

    def __dump_detail_xml(self):
        """
        导出详情页xml
        1.1.导出detail页面的xml数据，必须保障当前屏幕停留在详情页
        2.下载xml到本地
        """
        # 清理数据
        os.system("rm -f " + self.abs_detail_path)
        # 1.导出detail页面的xml数据，必须保障当前屏幕停留在详情页
        os.system("adb shell uiautomator dump /sdcard/bill_detail.xml")
        # 2.下载xml到本地
        os.system("adb pull /sdcard/bill_detail.xml " + self.abs_detail_path)

    def find_alipay_x_y(self):
        self.__dump_alipay_app_xml()
        result_list = load_xml(self.abs_alipay_app_path)
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.find("支付宝") >= 0:
                data = node.bounds
                data = str(data).replace('][', '|').replace('[', '').replace(']', '')
                datas = data.split("|")
                arr1 = str(datas[0]).split(",")
                arr2 = str(datas[1]).split(",")
                x = int(arr1[0]) + (int(arr2[0]) - int(arr1[0])) / 2
                y = int(arr1[1]) + (int(arr2[1]) - int(arr1[1])) / 2
                return x, y

    def notify_list(self):
        """
        统计支付宝支付通知条数
        :return: 通知总数
        """
        self.__dump_alipay_notify_xml()
        result_list = load_xml(self.abs_alipay_notify_path)
        count = 0
        for result in result_list:
            if Node().to_obj(result).text.__eq__("支付宝通知"):
                count += 1

        return count

    def detail(self):
        """
        转换xml数据，并提取关键数据，返回json格式数据
        :return: json格式数据
        """
        self.__dump_detail_xml()
        result_list = load_xml(self.abs_detail_path)
        data = {
            "user": Node().to_obj(result_list[3]).text,
            "orderNo": Node().to_obj(result_list[11]).text,
            "money": Node().to_obj(result_list[4]).text.replace("+", ""),
            "state": Node().to_obj(result_list[5]).text,
            "time": Node().to_obj(result_list[9]).text
        }
        return data

    def get_alipay_account(self):
        """
        获取支付宝账户信息
        :return: 支付宝账户
        """
        if self.is_personal_apge():
            result_list = load_xml(self.abs_personal_path)
            for result in result_list:
                node = Node().to_obj(result)
                if node.text.__eq__("支付宝账号"):
                    index = result_list.index(result)
                    alipay_account = Node().to_obj(result_list[index + 1]).text
                    return alipay_account
        else:
            return None

    def find_page_keywords(self, keyworkds, frequency=1):
        """
        根据支付宝页面的关键词进行检查当前是否在当前页，关键词比如 “我的” 是
        我的页面的关键词，出现2次，频率为2次匹配才算在指定页面，默认最少1次
        :param keyworkds: 关键词，一般为页面独一为二的关键词
        :param frequency: 出现在特殊页面的频次
        :return: True/False
        """
        self.__dump_x_page_xml()
        result_list = load_xml(self.abs_x_path)
        count = 0
        for result in result_list:
            node = Node().to_obj(result)
            if node.text.__eq__(keyworkds):
                count += 1
        if count >= frequency:
            return True
        else:
            return False

    def is_personal_apge(self):
        """
        是否是个人页面
        :return:True/False
        """
        self.__dump_personal_page_xml()
        is_personal = False
        is_personal_page = False
        result_list = load_xml(self.abs_personal_path)
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

    def is_user_center_page(self):
        """
        判断当前支付宝所在页面是否是 "我的" 页面
        :return:True/False
        """
        self.__dump_my_page_xml()
        is_my = False
        is_bill = False
        result_list = load_xml(self.abs_my_path)
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

    def get_bill_click_x_y(self):
        """
        获取 账单的点击坐标 x y
        :return:
        """
        if self.is_user_center_page():
            self.__dump_bill_coordinate_page_xml()
            result_list = load_xml(self.abs_bill_coordinate_path)
            for result in result_list:
                node = Node().to_obj(result)
                if node.text.__eq__("账单"):
                    data = node.bounds
                    data = str(data).replace('][', '|').replace('[', '').replace(']', '')
                    datas = data.split("|")
                    arr = str(datas[1]).split(",")
                    x = int(arr[0])
                    y = int(arr[1]) - 20
                    return x, y
        else:
            return False

    def income_list(self, num=5):
        """
        获取收入的列表
        :param num:　读取多少条默认５条
        :return: list
        """
        self.__dump_bill_page_xml()
        result_list = load_xml(self.abs_bill_path)
        income_list = list()
        for income in result_list:
            data = {
                "user": None,
                "money": 0,
                "goods": None,
                "today": None,
                "time": None,
                "click_x_y": None,
            }
            node = Node().to_obj(income)
            if node.text.find("收钱码收款") >= 0:
                index = result_list.index(income)
                for i in range(num):
                    try:
                        node_data = Node().to_obj(result_list[index + i])
                        if i == 0:
                            data["user"] = node_data.text.replace("收钱码收款-来自", "")
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


if __name__ == '__main__':
    alipay = AlipayXmlData()
    print(alipay.detail())
    # print(alipay.is_user_center_page())
    # print(alipay.is_personal_apge())
    # print(alipay.get_alipay_account())
    # print(alipay.get_bill_click_x_y())
    # print(alipay.income_list())
