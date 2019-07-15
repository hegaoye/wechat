import time

from src.service.paysv import PaySV


class Main:
    def configure(self):
        """
        上线并获取基本信息给到服务器端
        :return:
        """
        pay_sv = PaySV()
        return pay_sv.configure()

    def run(self, frequency=3):
        """
        开启监听支付结果
        :param frequency: 监听频率
        """
        pay_sv = PaySV()
        while True:
            is_notify = pay_sv.detect_alipay_notify()
            if is_notify:
                pay_sv.detect_income()
            else:
                time.sleep(frequency)


if __name__ == '__main__':
    try:
        app = Main()
        # flag = app.configure()
        # if flag:
        #     app.run()
        app.run()
    except Exception as e:
        print(e)
