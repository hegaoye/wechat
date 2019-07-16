from enum import Enum


class XMLPath(Enum):
    ALIPAY_APP = "alipay_app.xml"
    NOTIFY = "notify.xml"
    BILL_DETAIL = "bill_detail.xml"
    MY_PAGE = "my_page.xml"
    PERSONAL_PAGE = "personal_page.xml"
    X_PAGE = "x_page.xml"
    BILL_COORDINATE_PAGE = "bill_coordinate_page.xml"
    BILL_LIST_PAGE = "bill_list_page.xml"
    ABS_ALIPAY_APP_PATH = "/tmp/" + ALIPAY_APP.value
    ABS_ALIPAY_NOTIFY_PATH = "/tmp/" + NOTIFY.value
    ABS_DETAIL_PATH = "/tmp/" + BILL_DETAIL.value
    ABS_MY_PATH = "/tmp/" + MY_PAGE.value
    ABS_PERSONAL_PATH = "/tmp/" + PERSONAL_PAGE.value
    ABS_X_PATH = "/tmp/" + X_PAGE.value
    ABS_BILL_COORDINATE_PATH = "/tmp/" + BILL_COORDINATE_PAGE.value
    ABS_BILL_PATH = "/tmp/" + BILL_LIST_PAGE.value

    Sdcard_Path = "/sdcard/" + ALIPAY_APP.value
