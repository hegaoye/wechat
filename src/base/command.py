from enum import Enum

"""
设置等指令枚举
"""


class Command(Enum):
    Detect = "Detect"
    Sleep = "Sleep"
    Sys_Init = "Init"
    Sys_Login = "Login"
    Sys = "Sys"
    Host = "Host"
    Appkey = "Appkey"
    App_x_y = "App_x_y"
    Bill_x_y = "Bill_x_y"
    Scroll_Page_Size = "Scroll_Page_Size"
    Screen_x_y = "Screen_x_y"
