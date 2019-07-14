import time

from src.service.paysv import PaySV


class Main:
    def configure(self):
        """
        上线并获取基本信息给到服务器端
        :return:
        """

    def run(self, frequency=3):
        """
        开启监听支付结果
        :param frequency: 监听频率
        """
        pay_sv = PaySV()
        while True:
            is_detect = pay_sv.load_cmd()
            if is_detect:
                pay_sv.detect_income()
            else:
                time.sleep(frequency)


if __name__ == '__main__':
    app = Main()
    app.run()
