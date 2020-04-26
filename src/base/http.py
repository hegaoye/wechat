# coding=utf-8
from urllib import request, parse

from src.base.log4py import logger
from src.base.r import R


def get(url):
    # setting_dao = SettingDao()
    # host_setting = setting_dao.load(Command.Host)
    # url = host_setting["v"] + url
    logger.debug("请求url: " + url)
    response = request.urlopen(url)
    result = response.read().decode(encoding='utf-8')
    if result != None:
        beanret = R()
        beanret.to_obj(result)
        return beanret


def post(url, data=None, headers=None):
    try:
        logger.info(url)
        # setting_dao = SettingDao()
        # host_setting = setting_dao.load(Command.Host)
        # url = host_setting["v"] + url
        postdata = parse.urlencode(data).encode('utf-8')
        logger.info("请求url: " + url)
        logger.info("请求参数: " + str(postdata))
        if headers:
            req = request.Request(url, data=postdata, method="POST", headers=headers)
        else:
            req = request.Request(url, data=postdata, method="POST")
        response = request.urlopen(req)
        result = response.read().decode(encoding='utf-8')
        beanret = R().to_obj(result)
        return beanret
    except Exception as e:
        print(e)
        return R(success=False)
