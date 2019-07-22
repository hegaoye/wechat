# coding=utf-8
import datetime
import time

from src.base.beanret import BeanRet
from src.base.command import Command
from src.base.http import post
from src.base.log4py import logger
from src.base.md5 import md5
from src.dao.account_dao import AccountDao
from src.dao.bill_dao import BillDao
from src.dao.device_dao import DeviceDao
from src.dao.setting_dao import SettingDao
from src.service.alipay import AliPay


class PaySV:
    def __init__(self, device_id, debug=False):
        self.debug = debug
        self.device_id = device_id
        self.alipay = AliPay(device_id, debug)
        self.bill_dao = BillDao()
        self.account_dao = AccountDao()
        self.device_dao = DeviceDao()
        self.page_count = int(self.alipay.setting_dao.load(Command.Scroll_Page_Size)["v"])
        self.count_repeat = int(self.alipay.setting_dao.load(Command.Count_Repeat)["v"])

    def detect_income(self, alipay_account):
        """
        监听是否有新的支付订单
        １.进入账单页面
        ２.读取订单列表
        ３.读取订单详情
        ４.验证订单是否重复
        ５.提交订单
        ６.缓存结果
        :return:
        """
        # １.进入账单页面
        self.alipay.back_to_desktop()
        # 打开支付宝
        self.alipay.open_alipay_app(self.device_id)
        # 进入账单页面
        self.alipay.entry_bill_list_page()
        # 清理过期的数据
        self.delete_bill()

        # ２.读取订单列表
        count_repeat = 0
        for page in range(self.page_count):
            income_list = self.alipay.income_list()
            if income_list.__len__() <= 0:
                continue
            for income in income_list:
                if count_repeat == int(self.count_repeat):
                    break

                # ３.读取订单详情
                chick_x_y = income["click_x_y"]
                data = self.alipay.order_detail(chick_x_y[0], chick_x_y[1])
                self.alipay.back()

                # ４.验证订单是否重复
                order_no = data["orderNo"]

                bill_record = self.bill_dao.load(order_no)
                if bill_record:
                    logger.debug("重复单跳过，进行下一个")
                    count_repeat += 1
                    continue

                # ５.提交订单
                setting_dao = SettingDao()
                appkey_setting = setting_dao.load(Command.App)
                if not appkey_setting:
                    break
                appkey = appkey_setting["v"]

                account_dao = AccountDao()
                account_user = account_dao.load_by_account_appkey(alipay_account, appkey)
                if not account_user:
                    break

                user = data["user"]
                money = data["money"]
                state = data["state"]
                time_str = data["time"]

                # md5(money=&orderNo=&state=&time=&user= [appkey])
                text = "money=" + str(money) + "&orderNo=" + str(order_no) + "&state=" + str(state) + \
                       "&time=" + str(time_str) + "&user=" + str(user) + appkey

                logger.debug(text)
                sign = md5(text)
                logger.debug(sign)
                data["sign"] = sign

                header = {
                    'authorization': account_user["token"]
                }

                new_record_Url = self.alipay.setting_dao.load(Command.New_Record_Url)
                if not new_record_Url:
                    return

                if self.debug:
                    beanret = BeanRet()
                    beanret.success = True
                    beanret.data = "login_success"
                else:
                    beanret = post(new_record_Url["v"], data, header)

                if beanret.success:
                    # ６.缓存结果
                    bill_obj = self.bill_dao.load(order_no)
                    if not bill_obj:
                        account = self.account_dao.load_by_device_id(self.device_id)
                        if account:
                            self.bill_dao.insert(order_no, user, money, state, sign, time_str, account["account"])
                            logger.debug("新增一单: " + user)

            # 翻页计算
            if self.page_count - 1 - page > 0:
                income_0 = income_list[0]
                income_last = income_list[income_list.__len__() - 1]
                x1_y1 = income_0["click_x_y"]
                x2_y2 = income_last["click_x_y"]
                if x2_y2[1] >= x1_y1[1]:
                    self.alipay.scroll_down(x1_y1[0], 1080, x1_y1[0], 480)
                else:
                    self.alipay.scroll_down(x1_y1[0], 1080, x1_y1[0], x1_y1[1])
                time.sleep(.5)

        self.alipay.back_to_desktop()
        time.sleep(.3)

    def detect_connect(self):
        logger.debug("设备链接检测")
        return self.alipay.detect_connect(self.device_id)

    def device_list(self):
        """
        设备列表
        :return: device_list
        """
        device_list = self.alipay.detect_all_devices()
        return device_list

    def detect_alipay_notify(self):
        """
        监听支付宝的通知信息
        :return: True/False
        """
        logger.debug("监听支付宝的通知信息")
        return self.alipay.detect_alilpay_notify(self.device_id)

    def configure(self):
        """
        登录系统
        :return: True/False
        """
        self.alipay.back_to_desktop()
        self.alipay.open_alipay_app(self.device_id)
        self.alipay.jump_to_my_page()
        account, accountName, taobao_account = self.alipay.get_alipay_account(self.device_id)
        if not account or not accountName or not taobao_account:
            return
        appkey_setting = self.alipay.setting_dao.load(Command.App)
        if not appkey_setting:
            return
        appkey = appkey_setting["v"]

        data = {
            "account": account,
            "accountName": accountName,
            "appkey": appkey,
            "sign": md5("account=" + account + "&accountName=" + accountName + "&appkey=" + appkey + appkey)
        }

        login_url_setting = self.alipay.setting_dao.load(Command.Login_Url)
        if not login_url_setting:
            return

        if self.debug:
            beanret = BeanRet()
            beanret.success = True
            beanret.data = "login_success"
        else:
            beanret = post(login_url_setting['v'], data)

        if beanret.success:
            # 设置屏幕分辨率
            screen_x_y = self.alipay.screen_resolution()
            # 设置最大重复数多少时跳出
            count_Repeat_setting = self.alipay.setting_dao.load(Command.Count_Repeat)
            if not count_Repeat_setting:
                self.alipay.setting_dao.insert(Command.Count_Repeat, 3)

            token = str(beanret.data)
            account_load = self.account_dao.load_by_account(account)
            if account_load:
                self.account_dao.delete(self.device_id)

            self.account_dao.insert(account, appkey, token, self.device_id, screen_x_y)

            logger.debug("初始化配置完成")
            return True, account
        else:
            return False, account

    def delete_bill(self):
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=-2)
        re_date = (today + offset).strftime('%Y%m%d')
        self.bill_dao.delete_by_time(re_date + "000000")

    def load_device_by_id(self, device_id):
        """
        查询一个设备
        :param device_id: 设备id
        :return: 设备
        """
        return self.device_dao.load(device_id)

    def load_device(self):
        return self.device_dao.loadone()

    def save_device(self, device_id):
        self.device_dao.insert(device_id)

    def update_device(self, device_id):
        self.device_dao.update(device_id)

    def delete_device(self, device_id):
        self.device_dao.delete_by_id(device_id)

    def clear_device(self):
        self.device_dao.delete()
