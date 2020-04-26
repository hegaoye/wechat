# coding=utf-8
import threading

from src.base.log4py import logger
from src.service.art_of_war import ArtOfWar

"""
多线程启动不同设备
"""


class ProcessJimmy(threading.Thread):
    def __init__(self, device_id, frequency=1, debug=False):
        threading.Thread.__init__(self)
        self.device_id = str(device_id)
        self.debug = debug
        self.frequency = frequency
        self.is_stop = False

    def stop(self):
        '''
        stop thread
        :return:
        '''
        logger.debug("stop thread ! ")
        self.is_stop = True
        self.join()

    def run(self):
        '''
        running thread
        :return:
        '''
        logger.debug("running thread for device [" + self.device_id + "] ")

        try:
            ArtOfWar(self.device_id).run_sand_jimmy()
            # ArtOfWar(self.device_id).run_jimmy()
            logger.debug("connected to device:" + self.device_id)

        except:
            logger.debug("lost device: " + self.device_id)
