# coding=utf-8
import logging.config
import time

from src.service.paysv import PaySV


class Main:
    def __init__(self):
        self.pay_sv = PaySV()

    def configure(self):
        """
        上线并获取基本信息给到服务器端
        :return:
        """
        return self.pay_sv.configure()

    def run(self, frequency=3):
        """
        开启监听支付结果

        :param frequency: 监听频率
        """
        is_connected = False
        while True:
            try:
                if not is_connected:
                    is_connected = self.pay_sv.detect_connect()

                if is_connected:
                    is_notify = self.pay_sv.detect_alipay_notify()
                    if is_notify:
                        self.pay_sv.detect_income()
                    else:
                        time.sleep(frequency)
            except:
                is_connected = False
                log.debug("设备丢失")
                time.sleep(.5)


if __name__ == '__main__':

    try:
        logging.config.fileConfig('logging.conf')
        log = logging.getLogger(__name__)
        log.info('>>>>> Starting server <<<<<')
        app = Main()
        # flag = app.configure()
        # if flag:
        #     app.run()
        app.run()
    except Exception as e:
        print(e)
