# coding=utf-8

import re


def match(text, pattern) -> str:
    """
    正则匹配字符串
    :param text: 元数据必须是字符串
    :param pattern: 正则表达式 格式 r"xxx"
    :return: 匹配的结果
    """
    if type(text) == str:
        result = re.match(pattern, text)
        return result
    else:
        return None
