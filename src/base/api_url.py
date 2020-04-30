from enum import Enum


class Api(Enum):
    Host = "http://www.rzhkj.com/"

    """
    微信信息接口 post 推送获取的通讯录，群聊列表，微信个人信息
    """
    Wechat_Info_Url = Host + "/wechat/info"

    """
    获取任务 get 根据ip，序列号获取当前设备的任务
    """
    Get_Task_Url = Host + "xxx.shtml?serialno={serialno}&ip={ip}"

    """
    获取新设备 get 获取可能上线的新设备列表
    """
    Device_New_Url = Host + "device/new"

    """
    设备上线 post 设备成功上线后将会通知云端，云端对设备状态进行修改
    """
    Device_Online_Url = Host + "device/online"


if __name__ == '__main__':
    print(Api.Wechat_Info_Url.value)
