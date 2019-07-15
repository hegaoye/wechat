from src.base.command import Command
from src.base.http import post
from src.base.md5 import md5
from src.dao.account_dao import AccountDao
from src.dao.bill_dao import BillDao
from src.dao.setting_dao import SettingDao
from src.service.alipay import AliPay
from src.service.basesv import BaseSV


class PaySV(BaseSV):

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
        alipay = AliPay()
        alipay.jump_to_my_page()

        # ２.读取订单列表
        income_list = alipay.income_list()
        for income in income_list:
            # ３.读取订单详情
            chick_x_y = income["chick_x_y"]
            data = alipay.order_detail(chick_x_y[0], chick_x_y[1])
            alipay.back()

            # ４.验证订单是否重复
            order_no = data["orderNo"]
            bill_dao = BillDao()
            bill_record = bill_dao.load(order_no)
            if bill_record:
                continue

            # ５.提交订单
            setting_dao = SettingDao()
            appkey_setting = setting_dao.load(Command.Appkey)
            if not appkey_setting:
                return
            appkey = appkey_setting["v"]

            account_dao = AccountDao()
            account_user = account_dao.load(appkey)
            if not account_user:
                return

            user = data["user"]
            money = data["money"]
            state = data["state"]
            time_str = data["time"]
            text = str(order_no) + "&" + str(user) + "&" + str(money) + "&" + str(state) + "&" + str(
                time_str) + "&" + appkey

            sign = md5(text)
            data["sign"] = sign
            data["token"] = account_user["token"]
            beanret = post(self.new_record_Url, data)
            if beanret.success:
                # ６.缓存结果
                bill_dao.insert(order_no, user, money, state, sign, time_str)

    def detect_alipay_notify(self):
        """
        监听支付宝的通知信息
        :return: True/False
        """
        alipay = AliPay()
        return alipay.detect_alilpay_notify()

    def configure(self):
        """
        登录系统
        :return: True/False
        """
        alipay = AliPay()
        alipay.jump_to_my_page()
        account = alipay.get_alipay_account()
        if not account:
            return
        setting_dao = SettingDao()
        appkey_setting = setting_dao.load(Command.Appkey)
        if not appkey_setting:
            return
        appkey = appkey_setting["v"]

        data = {
            "account": account,
            "appkey": appkey,
            "sign": md5(account + "&" + appkey + "&" + appkey)
        }

        beanret = post(self.configure_Url, data)
        if beanret.success:
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
