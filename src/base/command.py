from enum import Enum


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
