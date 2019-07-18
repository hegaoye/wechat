import logging
import threading
import time

from src.service.paysv import PaySV

log = logging.getLogger(__name__)

"""
多线程启动不同设备
"""


class Process(threading.Thread):
    def __init__(self, device_id, frequency=3):
        threading.Thread.__init__(self)
        self.device_id = str(device_id)
        self.pay_sv = PaySV(str(device_id))
        self.frequency = frequency
        self.is_stop = False

    def stop(self):
        '''
        stop thread
        :return:
        '''
        log.debug("stop thread ! ")
        self.is_stop = True
        self.join()

    def run(self):
        '''
        running thread
        :return:
        '''
        log.debug("running thread ! ")
        is_connected = False
        is_login = False
        while True:
            if self.is_stop:
                log.debug("return while")
                return

            try:
                if not is_connected:
                    is_connected = self.detect_connect()

                if is_connected:
                    log.debug("connected device:" + self.device_id)
                    if not is_login:
                        is_login, alipay_account = self.configure()

                    if is_login:
                        is_notify = self.pay_sv.detect_alipay_notify()
                        if is_notify:
                            self.pay_sv.detect_income(alipay_account)
                        else:
                            time.sleep(self.frequency)
            except:
                is_connected = False
                is_login = False
                self.pay_sv.clear_login_cache()
                log.debug("lost device: " + self.device_id)
                time.sleep(.5)

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
