# coding=utf-8
import logging.config
import time

from src.base.file_tool import FileTool
from src.base.xml_path_enum import XMLPath
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
        """
        系统的入口
        :param frequency: 休眠频率 秒 为单位
        """
        list = self.device_list()
        if list:
            # 为设备创建临时工作目录
            for device_id in list:
                self.file_tool.remove(XMLPath.Workspace_PATH.value + str(device_id))
                self.file_tool.create_folder(XMLPath.Workspace_PATH.value + str(device_id))

            for device_id in list:
                process_thread = None
                try:
                    process_thread = Process(str(device_id), frequency, debug)
                    process_thread.start()
                    time.sleep(1)
                except:
                    log.debug("异常退出设备 : " + str(device_id))
                    if process_thread:
                        process_thread.stop()

        log.debug("线程启动完毕")


if __name__ == '__main__':
    try:
        logging.config.fileConfig('logging.conf')
        log = logging.getLogger(__name__)
        log.info('>>>>> Starting server <<<<<')
        # Main().run(debug=False)
        PaySV(None).delete_bill()

    except Exception as e:
        print(e)
