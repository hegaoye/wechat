import threading
from time import sleep

from src.base import http
from src.wechat.wechat_thread import WechatThread


class FactoryThread(threading.Thread):
    """
    微信设备工厂，自动连接设备并创建微信线程 (工厂仅允许单例模式)
    """

    def __init__(self):
        self.devices = []

    def run(self):
        while True:
            self.init_device()
            sleep(60)

    def __try_get_device(self) -> list:
        """
        尝试获取群发任务
        :return:
        """
        beanret = http.get(url="http://xxxx.com/device/new")
        if beanret.success:
            return beanret.data

    def __device_online(self, ip_list):
        """
        设备上线告知云端
        :param ip_list: 设备ip
        :return:
        """
        http.post("http://xxx.com/device/online", data={
            "ip": ip_list
        })

    def init_device(self):
        """
        初始化连接设备
        :return:
        """
        ip_list = self.__try_get_device()
        if len(ip_list) <= 0: return

        # 排除已经上线的设备
        if len(self.devices) > 0:
            for d in self.devices:
                ip = str(d["ip"])
                if ip in ip_list:
                    ip_list.remove(ip)

        if len(ip_list) > 0:
            online_devices = []
            for ip in ip_list:
                wechat_thread = WechatThread(ip)
                wechat_thread.start()
                device = {
                    "ip": str(ip),
                    "serialno": wechat_thread.wechat.serial(),
                    "wechat": wechat_thread
                }
                self.devices.append(device)
                online_device = {
                    "ip": str(ip),
                    "serialno": wechat_thread.wechat.serial(),
                    "status": "Online"
                }
                online_devices.append(online_device)

            # 设备上线告知云端
            self.__device_online(online_devices)


if __name__ == '__main__':
    wxt = FactoryThread()
