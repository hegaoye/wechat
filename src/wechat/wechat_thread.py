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
            self.wechat = Wechat(self.ip)
            # self.wechat.app_start()
            # myself_info, contacts, groups = self.wechat.init_wx()
            # self.post_wechat_info(myself_info, contacts, groups)

        while True:
            # 获取信息
            # info, contacts = self.try_get_task()
            info="代码已经提交，看群里，有地址说明可以下载后研究，具体细节这里在优化提交中"
            contacts=["立坤", "AAA . 立心", "小鹏", "伯融"]
            # 群发信息
            self.wechat.batch_send_msg(info, contacts)
            # 休眠1分钟再尝试获取任务
            sleep(60)

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
    wxt = WechatThread("192.168.0.28")
    wxt.start()
