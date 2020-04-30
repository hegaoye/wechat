from enum import Enum


class Api(Enum):
    Host = "http://www.rzhkj.com/"

    """
    微信信息接口
    """
    Wechat_Info_Url = Host + "/wechat/info"

    """
    获取任务
    """
    Get_Task_Url = Host + "xxx.shtml?serialno={serialno}&ip={ip}"

    """
    获取新设备
    """
    Device_New_Url = Host + "device/new"

    """
    设备上线
    """
    Device_Online_Url = Host + "device/online"


if __name__ == '__main__':
    print(Api.Wechat_Info_Url.value)
