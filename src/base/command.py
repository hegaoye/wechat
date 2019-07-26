# coding=utf-8
from enum import Enum

"""
设置等指令枚举
"""


class Command(Enum):
    Detect = "Detect"
    Sleep = "Sleep"
    Host = "Host"
    App = "App"
    APP_Secret = "APP_Secret"
    App_x_y = "App_x_y"
    Bill_x_y = "Bill_x_y"
    Scroll_Page_Size = "Scroll_Page_Size"
    Screen_x_y = "Screen_x_y"
    Count_Repeat = "Count_Repeat"
    Login_Url = "Login_Url"
    New_Record_Url = "New_Record_Url"
