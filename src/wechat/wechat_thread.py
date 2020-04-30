import threading
from time import sleep

from src.base import http
from src.base.api_url import Api
from src.base.log4py import logger
from src.wechat.wechat import Wechat


class WechatThread(threading.Thread):
    """
    微信多线程
    """

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.wechat = Wechat(self.ip)

    def run(self):
        logger.info("开始控制ip:" + str(self.ip))
        # 进行wx的初始化准备
        self.try_init_wx()
        while True:
            # 获取信息
            info, contacts = self.try_get_task()
            # 群发信息
            self.wechat.batch_send_msg(info, contacts)
            # 休眠1分钟再尝试获取任务
            sleep(60)

    def try_init_wx(self):
        """
        进行wx的初始化准备
        :return:
        """
        self.wechat.app_start()
        self.wechat.get_bottom_x_y()
        myself_info, contacts, groups = self.wechat.init_wx()
        self.post_wechat_info(myself_info, contacts, groups)

    def try_get_task(self):
        """
        尝试获取群发任务
        :return:
        """
        beanret = http.get(url=str(Api.Get_Task_Url.value)
                           .replace("{serialno}", str(self.wechat.serial))
                           .replace("{ip}", str(self.ip)))
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
        http.post(Api.Wechat_Info_Url.value, data=data)


if __name__ == '__main__':
    wxt1 = WechatThread("192.168.0.28")
    wxt1.start()
    sleep(3)
    wxt2 = WechatThread("192.168.0.23")
    wxt2.start()
