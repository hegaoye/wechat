import time

from src.base.beanret import BeanRet
from src.base.command import Command
from src.base.log4py import logger
from src.base.md5 import md5
from src.dao.account_dao import AccountDao
from src.dao.bill_dao import BillDao
from src.dao.setting_dao import SettingDao
from src.service.alipay import AliPay
from src.service.basesv import BaseSV


class PaySV(BaseSV):
    def __init__(self):
        self.alipay = AliPay()
        self.page_count = int(self.alipay.setting_dao.load(Command.Scroll_Page_Size)["v"])
        self.count_repeat = int(self.alipay.setting_dao.load(Command.Count_Repeat)["v"])

    def detect_income(self):
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
        self.alipay.open_alipay_app()
        self.alipay.entry_bill_list_page()

        # ２.读取订单列表
        count_repeat = 0
        for page in range(self.page_count):
            income_list = self.alipay.income_list()
            if income_list.__len__() <= 0:
                continue
            for income in income_list:
                if count_repeat == 2:
                    break

                # ３.读取订单详情
                chick_x_y = income["click_x_y"]
                data = self.alipay.order_detail(chick_x_y[0], chick_x_y[1])
                self.alipay.back()

                # ４.验证订单是否重复
                order_no = data["orderNo"]
                bill_dao = BillDao()
                bill_record = bill_dao.load(order_no)
                if bill_record:
                    print("重复单跳过，进行下一个")
                    count_repeat += 1
                    continue

                # ５.提交订单
                setting_dao = SettingDao()
                appkey_setting = setting_dao.load(Command.Appkey)
                if not appkey_setting:
                    break
                appkey = appkey_setting["v"]

                account_dao = AccountDao()
                account_user = account_dao.load(appkey)
                if not account_user:
                    break

                user = data["user"]
                money = data["money"]
                state = data["state"]
                time_str = data["time"]

                # md5(money=&orderNo=&state=&time=&user=&+appkey=)
                text = "money =" + str(money) + "&orderNo=" + str(order_no) + "&state=" + str(state) + \
                       "&time=" + str(time_str) + "&user=" + str(user) + "&appkey=" + appkey

                sign = md5(text)
                data["sign"] = sign
                data["token"] = account_user["token"]
                # TODO 调试后端接口
                beanret = BeanRet()
                beanret.success = True
                # beanret = post(self.new_record_Url, data)
                if beanret.success:
                    # ６.缓存结果
                    bill_obj = bill_dao.load(order_no)
                    if not bill_obj:
                        bill_dao.insert(order_no, user, money, state, sign, time_str)
                        print("新增一单: " + user)

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

    def detect_alipay_notify(self):
        """
        监听支付宝的通知信息
        :return: True/False
        """
        return self.alipay.detect_alilpay_notify()

    def configure(self):
        """
        登录系统
        :return: True/False
        """
        self.alipay.back_to_desktop()
        self.alipay.open_alipay_app()
        self.alipay.jump_to_my_page()
        account = self.alipay.get_alipay_account()
        if not account:
            return
        setting_dao = SettingDao()
        appkey_setting = setting_dao.load(Command.Appkey)
        if not appkey_setting:
            return
        appkey = appkey_setting["v"]

        data = {
            "account": account,
            "password": appkey,
            "sign": md5("account=" + account + "&password=" + appkey + "&appkey=" + appkey)
        }

        logger.debug(data)
        # TODO 调试后端接口
        beanret = BeanRet()
        beanret.success = True
        beanret.data = "you_are_logined"
        # beanret = post(self.configure_Url, data)

        if beanret.success:
            # 设置屏幕分辨率
            x_y = self.alipay.screen_resolution()
            setting_dao.insert(Command.Screen_x_y, x_y)
            # 设置最大重复数多少时跳出
            setting_dao.insert(Command.Count_Repeat, 3)

            setting = setting_dao.load(Command.Sys)
            account_dao = AccountDao()
            token = str(beanret.data)
            if str(setting["v"]).__eq__(Command.Sys_Init.value):
                setting_dao.update(Command.Sys, Command.Sys_Login.value)
                account_dao.insert(account, appkey, token)
            else:
                account_dao.update(account, token)

            return True
        else:
            return False
