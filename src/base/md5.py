import hashlib


def md5(text):
    m2 = hashlib.md5()
    m2.update(text)
    return m2.hexdigest()
