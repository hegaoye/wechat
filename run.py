# coding=utf-8
import logging.config

from src.base.file_tool import FileTool
from src.service.paysv import PaySV
from src.service.process import Process


class Main:
    def __init__(self):
        self.pay_sv = PaySV(None)
        self.file_tool = FileTool()

    def device_list(self):
        return self.pay_sv.device_list()

    def run(self, frequency=3):
        list = self.device_list()
        if list:
            # 创建不同的临时目录
            for device_id in list:
                self.file_tool.create_folder("/tmp/" + str(device_id))

            for device_id in list:
                process_thread = None
                try:
                    process_thread = Process(str(device_id), frequency)
                    process_thread.start()
                except:
                    log.debug("异常退出设备 : " + str(device_id))
                    if process_thread:
                        process_thread.stop()


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
