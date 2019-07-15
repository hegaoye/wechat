# coding=utf-8
import configparser

from settings import PITOP_CONF


class BaseSV:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read(PITOP_CONF, encoding='UTF-8')
        host = cf.get("sys", "host")
        self.host = host
        self.new_record_Url = ""
        self.load_cmd_Url = ""
        self.configure_Url = ""
