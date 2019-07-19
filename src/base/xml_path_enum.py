# coding=utf-8
from enum import Enum

"""
用于从手机导出xml页面文件的枚举配置
"""


class XMLPath(Enum):
    ALIPAY_APP = "alipay_app.xml"
    NOTIFY = "notify.xml"
    BILL_DETAIL = "bill_detail.xml"
    MY_PAGE = "my_page.xml"
    PERSONAL_PAGE = "personal_page.xml"
    X_PAGE = "x_page.xml"
    BILL_COORDINATE_PAGE = "bill_coordinate_page.xml"
    BILL_LIST_PAGE = "bill_list_page.xml"
    CONNECT = "connect.xml"

    # 本地地址
    ABS_ALIPAY_APP_PATH = "/tmp/{device_id}/" + ALIPAY_APP
    ABS_ALIPAY_NOTIFY_PATH = "/tmp/{device_id}/" + NOTIFY
    ABS_DETAIL_PATH = "/tmp/{device_id}/" + BILL_DETAIL
    ABS_MY_PATH = "/tmp/{device_id}/" + MY_PAGE
    ABS_PERSONAL_PATH = "/tmp/{device_id}/" + PERSONAL_PAGE
    ABS_X_PATH = "/tmp/{device_id}/" + X_PAGE
    ABS_BILL_COORDINATE_PATH = "/tmp/{device_id}/" + BILL_COORDINATE_PAGE
    ABS_BILL_PATH = "/tmp/{device_id}/" + BILL_LIST_PAGE
    ABS_CONNECT_PATH = "/tmp/{device_id}/" + CONNECT

    # 手机存储地址
    Sdcard_ABS_ALIPAY_APP_PATH = "/storage/emulated/0/" + ALIPAY_APP
    Sdcard_ABS_ALIPAY_NOTIFY_PATH = "/storage/emulated/0/" + NOTIFY
    Sdcard_ABS_DETAIL_PATH = "/storage/emulated/0/" + BILL_DETAIL
    Sdcard_ABS_MY_PATH = "/storage/emulated/0/" + MY_PAGE
    Sdcard_ABS_PERSONAL_PATH = "/storage/emulated/0/" + PERSONAL_PAGE
    Sdcard_ABS_X_PATH = "/storage/emulated/0/" + X_PAGE
    Sdcard_ABS_BILL_COORDINATE_PATH = "/storage/emulated/0/" + BILL_COORDINATE_PAGE
    Sdcard_ABS_BILL_PATH = "/storage/emulated/0/" + BILL_LIST_PAGE
    Sdcard_ABS_CONNECT_PATH = "/storage/emulated/0/" + CONNECT

    # 工作空间
    Workspace_PATH = "/tmp/"
