from src.base.http import post
from src.dao.bill_dao import BillDao
from src.service.alipay import AliPay
from src.service.basesv import BaseSV


class PaySV(BaseSV):

    def check_paid_order_no(self):
        """
        验证支付订单号服务器端是否已经存在
        1.获取订单号，付款信息，个人信息，交易状态，交易时间
        2.查询本地是否缓存存在
        3.发送云端验证，缓存本地
        :return:
        """
        alipay = AliPay()
        src_filename, order_no_img_path, order_money_img_path, order_state_img_path, order_time_img_path = alipay.crop_order_detail()
        # 1.获取订单号，付款信息，个人信息，交易状态，交易时间
        # 解析订单号
        order_no = alipay.image_to_text(order_no_img_path)
        # 2.查询本地是否缓存存在
        bill_dao = BillDao()
        bill_record = bill_dao.load(order_no)
        if bill_record:
            alipay.back()
            return

        # 3.发送云端验证，缓存本地
        order_money = alipay.image_to_text(order_money_img_path)
        order_state = alipay.image_to_text(order_state_img_path, "chi_sim")
        order_time = alipay.image_to_text(order_time_img_path)
        # TODO md5 签名 md5(order_no,money,state,time)
        sign = ""
        data = {
            "orderNo": str(order_no),
            "money": str(order_money),
            "state": str(order_state),
            "time": str(order_time),
            "sign": str(sign)
        }
        beanret = post(self.new_record_Url, data)
        if beanret.success:
            # bill_dao.insert(order_no,)
            alipay.back()
            pass
