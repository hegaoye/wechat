# coding=utf-8
import hashlib


def md5(text):
    m2 = hashlib.md5()
    m2.update(text.encode(encoding='utf-8'))
    return m2.hexdigest()
