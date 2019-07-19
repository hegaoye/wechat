import threading
import time

from src.base.log4py import logger
from src.service.paysv import PaySV

"""
多线程启动不同设备
"""


class Process(threading.Thread):
    def __init__(self, device_id, frequency=3, debug=False):
        threading.Thread.__init__(self)
        self.device_id = str(device_id)
        self.pay_sv = PaySV(str(device_id), debug=debug)
        self.frequency = frequency
        self.is_stop = False

    def stop(self):
        '''
        stop thread
        :return:
        '''
        logger.debug("stop thread ! ")
        self.is_stop = True
        self.join()

    def run(self):
        '''
        running thread
        :return:
        '''
        logger.debug("running thread for device [" + self.device_id + "] ")
        is_connected = False
        is_login = False
        while True:
            if self.is_stop:
                logger.debug("return while")
                return

            try:
                if not is_connected:
                    is_connected = self.detect_connect()

                if is_connected:
                    logger.debug("connected to device:" + self.device_id)
                    if not is_login:
                        is_login, alipay_account = self.configure()

                    if is_login:
                        is_notify = self.pay_sv.detect_alipay_notify()
                        if is_notify:
                            self.pay_sv.detect_income(alipay_account)
            except:
                is_connected = False
                is_login = False
                logger.debug("lost device: " + self.device_id)

            time.sleep(self.frequency)

    def configure(self):
        """
        上线并获取基本信息给到服务器端
        :return:
        """
        return self.pay_sv.configure()

    def detect_connect(self):
        """
        设备上线检测
        :return:
        """
        return self.pay_sv.detect_connect()
