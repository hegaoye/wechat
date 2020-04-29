# coding=utf-8
import logging.config

from settings import LOGGIN_CONF
from src.wechat.factory import FactoryThread

"""
入口启动文件类
"""


class Main:
    def run(self):
        wxt = FactoryThread()
        wxt.start()


if __name__ == '__main__':
    try:
        logging.config.fileConfig(LOGGIN_CONF)
        log = logging.getLogger(__name__)
        log.info('>>>>> Starting server <<<<<')
        Main().run()

    except Exception as e:
        print(e)
