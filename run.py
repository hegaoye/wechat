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

        while True:
            is_notify = self.pay_sv.detect_alipay_notify()
            if is_notify:
                self.pay_sv.detect_income()
            else:
                time.sleep(frequency)


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
