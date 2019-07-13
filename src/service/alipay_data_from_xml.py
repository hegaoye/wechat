import os

from src.service.parse_xml import load_xml


class AlipayXmlData:
    def __init__(self):
        self.abs_detail_path = "/home/scrapy_pay_client/bill_detail.xml"
        self.abs_my_path = "/home/scrapy_pay_client/my_page.xml"

    def __dump_my_page_xml(self):
        """
        导出我的页ui xml
        """
        os.system("rm -f " + self.abs_my_path)
        os.system("adb shell uiautomator dump /sdcard/my_page.xml")
        os.system("adb pull /sdcard/my_page.xml " + self.abs_my_path)

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

    def detail(self):
        """
        转换xml数据，并提取关键数据，返回json格式数据
        :return: json格式数据
        """
        self.__dump_detail_xml()
        result_list = load_xml(self.abs_detail_path)
        data = {
            "user": result_list[3][1],
            "orderNo": result_list[11][1],
            "money": str(result_list[4][1]).replace("+", ""),
            "state": result_list[5][1],
            "time": result_list[9][1]
        }
        print(data)
        return data

    def is_user_center_page(self):
        """
        判断当前支付宝所在页面是否是 "我的" 页面
        :return:True/False
        """
        self.__dump_my_page_xml()
        is_my = False
        is_bill = False
        result_list = load_xml(self.abs_my_path)
        for x in result_list:
            if str(x[1]).__eq__("我的"):
                is_my = True
            if str(x[1]).__eq__("账单"):
                is_bill = True

        if is_my and is_bill:
            return True
        else:
            return False


if __name__ == '__main__':
    alipay = AlipayXmlData()
    # alipay.detail()
    print(alipay.is_user_center_page())
