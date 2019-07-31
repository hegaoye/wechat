# coding=utf-8
import logging.config
import time

from settings import LOGGIN_CONF
from src.base.file_tool import FileTool
from src.base.log4py import logger
from src.base.xml_path_enum import XMLPath
from src.service.detect_device import DetectDevice
from src.service.paysv import PaySV
from src.service.process import Process

"""
入口启动文件类
"""


class Main:
    def __init__(self):
        self.pay_sv = PaySV(None)
        self.file_tool = FileTool()

    def device_list(self):
        """
        设备列表
        :return: 所有设备列表
        """
        return self.pay_sv.device_list()

    def run(self, frequency=3, debug=False):
        logger.info("启动设备上线检测")
        DetectDevice().start()

        logger.info("尝试启动上线的设备")
        while True:
            device_id = self.pay_sv.load_device()
            if device_id:
                self.file_tool.remove(XMLPath.Workspace_PATH.value + str(device_id))
                self.file_tool.create_folder(XMLPath.Workspace_PATH.value + str(device_id))
                process_thread = None
                try:
                    self.pay_sv.update_device(device_id)
                    process_thread = Process(str(device_id), frequency, debug)
                    process_thread.start()
                    logger.info("启动对设备[" + str(device_id) + "]的控制")
                    time.sleep(1)
                except:
                    log.error("异常退出设备 : " + str(device_id))
                    if process_thread:
                        process_thread.stop()
            else:
                time.sleep(3)


if __name__ == '__main__':
    try:
        logging.config.fileConfig(LOGGIN_CONF)
        log = logging.getLogger(__name__)
        log.info('>>>>> Starting server <<<<<')
        Main().run(debug=False)

    except Exception as e:
        print(e)
