# coding=utf-8
import logging.config

from settings import LOGGIN_CONF
from src.base.log4py import logger
from src.service.art_of_war_thread import Process
from src.service.art_of_war_thread_jimmy import ProcessJimmy

"""
入口启动文件类
"""


class Main:
    def run(self, frequency=1, debug=False):
        logger.info("尝试启动上线的设备")
        device_id = "S2D7N19328004812"
        try:
            # process_thread = Process(str(device_id), frequency, debug)
            # process_thread.start()

            device_id = "RELBB18A19500825"
            process_jimmy_thread = ProcessJimmy(str(device_id), frequency, debug)
            process_jimmy_thread.start()
            logger.info("启动对设备[" + str(device_id) + "]的控制")
        except:
            log.error("异常退出设备 : " + str(device_id))
            # if process_thread:
            #     process_thread.stop()

            if process_jimmy_thread:
                process_jimmy_thread.stop()


if __name__ == '__main__':
    try:
        logging.config.fileConfig(LOGGIN_CONF)
        log = logging.getLogger(__name__)
        log.info('>>>>> Starting server <<<<<')
        Main().run()

    except Exception as e:
        print(e)
