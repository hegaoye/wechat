import threading
import time

from src.base.log4py import logger
from src.service.paysv import PaySV

"""
多线程检测设备上线加入队列，下线移除队列
"""


class DetectDevice(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pay_sv = PaySV(None)

    def stop(self):
        '''
        stop thread
        :return:
        '''
        logger.info("stop thread ! ")
        self.is_stop = True
        self.join()

    def run(self):
        '''
        running thread
        1.获取设备列表
        2.数据运算，计算并保存新设备
        3.移除设备
        '''
        self.pay_sv.clear_device()
        while True:
            # 1.获取设备列表
            device_list = self.pay_sv.device_list()
            if device_list.__len__() > 0:
                # 2.数据运算，计算并保存新设备
                for device_id in device_list:
                    device = self.pay_sv.load_device_by_id(device_id)
                    if not device:
                        self.pay_sv.save_device(device_id)
                        logger.info("发现新设备[" + str(device_id) + "]")

            time.sleep(5)
