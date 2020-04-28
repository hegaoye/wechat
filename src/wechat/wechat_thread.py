import threading
from time import sleep

from src.base import http
from src.wechat.wechat import Wechat


class WechatThread(threading.Thread):
    """
    微信多线程
    """

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.wechat = None

    def run(self):
        if self.wechat is None:
            print("开始控制ip", self.ip)
            self.wechat = Wechat(self.ip)
            # self.wechat.get_bottom_x_y()
            # self.wechat.app_start()
            # myself_info, contacts, groups = self.wechat.init_wx()
            # print(groups)
            # self.post_wechat_info(myself_info, contacts, groups)

        while True:
            # 获取信息
            # info, contacts = self.try_get_task()
            info = """现货抢购

KN95 封边机
KN95 点焊机
KN95 鼻梁机

电话咨询 18703830130 
微信咨询 18589077222（勿打电话给此号）

全部现货，工厂直销可视频可看货可现场试机
不含税不含发票诚意需要的请联系"""

            # contacts = ["立坤", "AAA . 立心", "小鹏", "伯融"]
            # 群发信息
            # self.wechat.batch_send_msg(info, contacts)
            self.wechat.batch_send_msg_by_keyword(info, "口罩", except_contacts=["一家人", "口罩机销售"])
            # 休眠1分钟再尝试获取任务
            sleep(1800)

    def try_get_task(self):
        """
        尝试获取群发任务
        :return:
        """
        beanret = http.get(url="http://xxxx.com/xxx.shtml?serialno=" + str(self.wechat.serial) + "&ip=" + str(self.ip))
        if beanret.success:
            return beanret.data["info"], beanret.data["contacts"]

    def post_wechat_info(self, myself_info, contacts, groups):
        """
        初始化时向云端发送基础数据
        """
        data = {
            "myselfInfo": myself_info,
            "contact": contacts,
            "group": groups,
            "ip": str(self.ip),
            "serialno": str(self.wechat.serial)
        }
        http.post("http://xxxx.com/xxx.shtml", data=data)


if __name__ == '__main__':
    wxt1 = WechatThread("192.168.0.28")
    wxt1.start()
    sleep(3)
    wxt2 = WechatThread("192.168.0.23")
    wxt2.start()
