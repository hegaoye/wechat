# coding=utf-8
from time import sleep

import re

from src.base.appbase import AppBase
from src.base.log4py import logger


class Wechat(AppBase):
    """"
    用于控制 wechat 的封装，仅针对微信起作用，
    一下各个方法中有的出现了 resourceId,text,description 等内容
    用于获取元素，但这些可能发生变化，后期应存储于云端，采用云端配置，本地同步
    的机制，并开启多线程进行检测，或者mq进行监听变化进行更新及时修复错误
    """

    def __init__(self, ip):
        AppBase.__init__(self, ip)
        # 微信号
        self.wx_id = None
        # 微信汉字昵称
        self.nick_name = None
        # 联系人集合
        self.contacts = []
        # 群集合
        self.groups = []
        # 最大纵坐标
        self.max_y = 0

    def app_start(self):
        """
        启动微信软件，会自动到桌面上寻找微信
        :return:
        """
        self.home()
        sleep(.5)
        self.__try_to_find_wx_app()
        sleep(.5)
        logger.debug("启动 wechat")

    def init_wx(self):
        """
        初始化微信
        1.获取联系人通讯录信息
        2.获取群组信息
        :return:
        """
        self.get_bottom_x_y()
        logger.info("开始获取 微信账户信息")
        self.get_myself_info()
        myself_info = {"wxId": str(self.wx_id), "nickName": str(self.nick_name)}
        logger.info("开始获取 通讯录信息")
        contacts = self.get_contact_info()
        logger.info("开始获取 群 通讯录信息")
        groups = self.get_groups()
        return myself_info, contacts, groups

    def __try_to_find_wx_app(self):
        """
        查找微信app，自动向右翻页
        :return:
        """
        # 查找微信
        wx_app = self.d(text="微信")
        if not wx_app.exists():
            # 向右滑屏
            self.d(scrollable=True).fling.horiz.forward()
            # 迭代查找
            self.__try_to_find_wx_app()
        else:
            # 点击微信图标，启动微信
            wx_app.click()

    def get_contact_info(self) -> list:
        """
        读取通讯录信息 （所有信息）
        :return:
        """
        # 打开通讯录
        self.__contact_tab()
        # 获取联系人列表
        self.__list_contacts()
        return self.contacts

    def get_myself_info(self):
        """
        获取个人微信信息
        1.进入到我的标签页
        2.打开个人信息页面
        3.获取个人信息
        :return:
        """
        self.__myself_tab()
        self.__myself_info_page()
        self.__get_myself_info()
        # 返回上一页
        self.back()

    def __myself_tab(self):
        """
        打开 我 标签页
        :return:
        """
        myself_tab = self.d.xpath(
            '//*[@resource-id="com.tencent.mm:id/cwx"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[4]')
        myself_tab.click()
        sleep(.5)

    def __myself_info_page(self):
        """
        进入到 个人信息页面
        :return:
        """
        self.d(resourceId="com.tencent.mm:id/eje").click()
        sleep(.5)

    def __get_myself_info(self):
        """
        获取 个人信息页 中的 微信号，个人昵称，头像图片等信息
        :return:
        """
        name_element = self.d(resourceId="android:id/title", text="昵称").right(resourceId="android:id/summary")
        self.wx_id = name_element.get_text()
        wx_id_element = self.d(resourceId="android:id/title", text="微信号").right(resourceId="android:id/summary")
        self.nick_name = wx_id_element.get_text()
        print(self.nick_name, self.wx_id)
        sleep(.5)

    def __contact_tab(self):
        """
        打开通讯录
        """
        # 定位通讯录
        contact_tab = self.d.xpath(
            '//*[@resource-id="com.tencent.mm:id/cwx"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]')
        # 打开通讯录
        contact_tab.click()

    def __list_contacts(self):
        """
        查询所有的联系人，并制定去重，包括剔除自己
        :return:  联系人集合
        """
        try:
            # 获取当前页联系人列表
            contact_list = self.d(resourceId="com.tencent.mm:id/dux")
            if len(contact_list) > 0:
                contact_name_list = []
                for contact in contact_list:
                    contact_name_list.append(contact.get_text())

                # 去重联系人
                contact_name_list += self.contacts
                contact_name_set = set(contact_name_list)
                if len(contact_name_set) > len(self.contacts):
                    self.contacts = contact_name_set
                else:
                    return

            print(len(self.contacts), self.contacts)

            # 向下滑动
            self.d(scrollable=True).scroll.vert.forward(steps=100)
        except:
            # 等待超时后自动移动一部分尝试寻找新数据
            self.d(scrollable=True).scroll.vert.forward(steps=150)

        # 迭代循环
        self.__list_contacts()

    def get_groups(self) -> list:
        """
        读取微信的群，
        实现方式，通过读取通讯里把联系人进行临时存储，并在微信标签
        中翻页方式获取所有的聊天信息，并排除联系人，剩余的默认为群
        特殊的联系人如微信团队等，需要另外提出过滤即可
        :return:
        """
        self.__wx_tab()
        self.__list_groups()

        return self.groups

    def __wx_tab(self, is_to_end=True):
        """
        选择微信标签
        """
        # 点击微信标签
        wx_tab = self.d.xpath(
            '//*[@resource-id="com.tencent.mm:id/cwx"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
        wx_tab.click()
        if is_to_end:
            self.d(scrollable=True).fling.toEnd()

    def __list_groups(self):
        """
        获取聊天列表，并提出联系人即可
        :return:
        """
        if self.is_top():
            return

        wx_tab_element_list = self.d(className="android.view.View", resourceId="com.tencent.mm:id/e0n")
        if len(wx_tab_element_list) > 0:
            group_name_list = []
            for wx_tab_element in wx_tab_element_list:
                name = wx_tab_element.get_text()
                if name not in self.contacts:
                    group_name_list.append(name)

            # 去重群名
            group_name_list += self.groups
            group_name_set = set(group_name_list)
            if len(group_name_set) > len(self.groups):
                self.groups = group_name_set
            else:
                return
            print(len(self.groups), self.groups)

        # 向上滑动
        self.swipe_backward()
        # 迭代翻页获取所有的群
        self.__list_groups()

    def swipe_backward(self):
        """
        向上滑动
        :return:
        """
        self.d.swipe(194, 283, 194, 1447, .1)

    def is_top(self) -> bool:
        # 检查最先面的导航是否存在，不存在说明下拉刷新界面出现，需要终止
        myself_tab = self.d(resourceId="com.tencent.mm:id/cko")
        if not myself_tab.exists():
            self.d(scrollable=True).scroll(steps=10)
            return True
        else:
            return False

    def search_contact(self, name):
        """
        点击搜索框，并输入内容进行自动搜索
        :param name:
        :return:
        """
        self.__get_search_force()
        self.d.send_keys(name)
        sleep(1)

    def __get_search_force(self):
        """
        获取搜索框的光标
        :return:
        """
        search_element = self.d(resourceId="com.tencent.mm:id/dka", description="搜索")
        if search_element.exists():
            search_element.click()
            sleep(1)
        else:
            sleep(.5)
            self.__get_search_force()

    def open_search_result(self, name, try_nums=3) -> bool:
        """
        打开搜索的结果，并根据搜索的名字进行选择
        :param name: 搜索的名字
        :param try_nums: 检查元素不存在的次数统计，默认即可，无需传参
        """
        result_element = self.d(resourceId="com.tencent.mm:id/g8b", textContains=name)
        if result_element.exists():
            result_element[0].click()
            return True
        else:
            if try_nums <= 0:
                return False

            try_nums -= 1
            sleep(.5)
            return self.open_search_result(name, try_nums)

    def is_group(self) -> bool:
        """
        判断是否是群
        :return: True 是群 False 不是群
        """
        element = self.d(resourceId="com.tencent.mm:id/g7_")
        if not element.exists():
            return False

        name = element.get_text()
        if not name:
            return False

        is_group = re.search('\(\d+\)$', str(name))
        if is_group:
            return True
        else:
            return False

    def clear_search(self):
        """
        清理搜索框
        """
        clear_element = self.d(resourceId="com.tencent.mm:id/foi", description="清除")
        if clear_element.exists():
            clear_element.click()
            sleep(.5)
        else:
            sleep(.5)
            self.clear_search()

    def cancel_search(self):
        """
        取消搜索
        """
        cancel_element = self.d(resourceId="com.tencent.mm:id/aai", text="取消")
        if cancel_element.exists():
            cancel_element.click()
            sleep(.5)

    def send_msg(self, msg):
        """
        发送消息
        :param msg: 消息文字信息
        """
        # 光标定位到输入框中
        msg_input = self.d(resourceId="com.tencent.mm:id/g2p")
        if msg_input.exists():
            msg_input.click()
            sleep(1)
            self.d.send_keys(msg)
            logger.debug("发送消息内容为：" + msg)
            sleep(1)
            # 点击发送
            send_button = self.d(resourceId="com.tencent.mm:id/amr")
            if send_button.exists():
                send_button.click()
                sleep(1)
                # 对话返回
                self.dialog_back()
        else:
            sleep(.5)
            self.send_msg(msg)

    def dialog_back(self):
        """
        对话框返回
        """
        back_element = self.d(resourceId="com.tencent.mm:id/rm")
        if back_element.exists():
            # 点击左上角返回键
            logger.debug("点击左上角返回上一页")
            back_element.click()
            sleep(.5)
        else:
            # 系统默认返回键返回
            self.back()

    def batch_send_msg_by_search(self, text, contact_list) -> bool:
        """
        利用微信提供的头部搜索框方式搜索 名片进行发送消息，
        且搜索关键词为全词匹配模式
        :param text: 要发送的文本内容
        :param contact_list: 联系人名片集合
        :return True 发送成功 False 发送失败
        """
        if len(contact_list) <= 0:
            return False

        self.__get_search_force()

        for contact in contact_list:
            # 输入文字搜索名片
            self.d.send_keys(contact)
            sleep(1)
            # 打开搜索结果
            if self.open_search_result(contact):
                # 发送消息
                self.send_msg(text)

            # 清空搜索框
            self.clear_search()

        # 取消搜索返回微信聊天列表
        self.cancel_search()

        return True

    def batch_send_msg_by_keyword(self, msg, keyword, except_contacts):
        """
        通过搜索关键词来对应群组
        :param msg: 消息
        :param keyword: 搜索关键词
        :param except_contacts: 例外的通讯录
        :return:
        """
        self.__get_search_force()
        self.d.send_keys(keyword)
        self.d(scrollable=True).scroll.vert.forward(steps=10)
        sleep(1)
        self.try_open_group_more()
        self.__group_chat(msg, except_contacts)
        self.back()
        # self.cancel_search()
        sleep(.5)
        # self.cancel_search()
        self.back()

    def try_open_group_more(self, try_nums=5):
        """
        打开更多群聊的搜索结果列表
        :param try_nums: 尝试次数
        """
        element = self.d(resourceId="com.tencent.mm:id/g6i", text="更多群聊")
        if element.exists():
            element.click()
            sleep(1)
        else:
            if try_nums <= 0:
                return
            try_nums -= 1
            sleep(1)
            self.try_open_group_more(try_nums)

    def __group_chat(self, msg, except_contacts):
        """
        搜到的群聊列表，选择性打开，如果有例外的则自动排除
        :param msg: 消息体
        :param except_contacts: 例外列表
        """
        group_chat_list = self.d(resourceId="com.tencent.mm:id/g8b")
        if len(group_chat_list) > 0:
            for group_chat in group_chat_list:
                group_name = group_chat.get_text()
                if not group_name:
                    continue

                # 名字中出现 (数字) 的进行替换
                group_name = re.sub(r"\(\d+\)$", "", str(group_name))
                if group_name in except_contacts:
                    continue

                except_contacts.append(group_name)
                if len(except_contacts) >= 80:
                    return
                group_chat.click()
                self.send_msg(msg)

            self.d(scrollable=True).scroll.vert.forward(steps=50)
            sleep(1)
            self.__group_chat(msg, except_contacts)

    def batch_send_msg(self, text, contact_list):
        """
        群发消息，根据策略不同选择的发送方式不同
        :param text: 需要发送的文本内容
        :param contact_list: 联系人列表
        """
        # if len(contact_list) > 0 and len(contact_list) > 10:
        #     # 滚动翻页群发
        #     self.batch_send_msg_by_scroll(text, contact_list)
        # else:
        # 搜索定向发送
        self.batch_send_msg_by_search(text, contact_list)

    def batch_send_msg_by_scroll(self, text, contact_list):
        """
        批量发送消息
        :param msg:
        :param contact_list:
        """
        self.__wx_tab(False)
        self.__batch_send_msg(text, contact_list)

    def __send_first_page(self, text, contact_list) -> bool:
        """
        针对第一屏进行发送处理
        :param text: 要发送的文本内容
        :param contact_list: 名表列表
        :return: True 可以继续发送  False 无需继续发送
        """
        dialogs = self.d(className="android.view.View", resourceId="com.tencent.mm:id/e0n")
        if len(dialogs) > 0:
            for dialog in dialogs:
                dialog_name = dialog.get_text()
                if dialog_name in contact_list:
                    dialog_height = dialog.center()[1]
                    if int(dialog_height) > self.max_y:
                        continue

                    dialog.click()
                    sleep(.5)
                    # 发送消息
                    self.send_msg(text)
                    # 删除发送过消息的列表信息
                    contact_list.remove(dialog_name)
                    if len(contact_list) == 0:
                        return False

        return True

    def __batch_send_msg(self, msg, contact_list):
        """
        批量发送消息 具体实现，向上滑动，查找元素是否在
        contact_list 中，如果有则打开对话框->发送消息->返回->删除发送过的名字->向上滑动，寻找新的
        继续发送消息直到滑到顶端或者联系集合空为止
        :param msg:
        :param contact_list:
        :return:
        """
        # 顶部停止
        # if self.is_top():
        #     return

        dialogs = self.d(className="android.view.View", resourceId="com.tencent.mm:id/e0n")
        if len(dialogs) > 0:
            for dialog in dialogs:
                dialog_name = dialog.get_text()
                if dialog_name in contact_list:
                    dialog_height = dialog.center()[1]
                    if int(dialog_height) > self.max_y:
                        continue
                    dialog.click()
                    if not self.is_group():
                        continue
                    print("操作", dialog_name)
                    # 发送消息
                    self.send_msg(msg)
                    # 删除发送过消息的列表信息
                    contact_list.remove(dialog_name)
                    if len(contact_list) == 0:
                        return

            # 向下滚动
            self.d(scrollable=True).scroll.vert.forward(steps=50)
            # 递归查找
            self.__batch_send_msg(msg, contact_list)

    def get_bottom_x_y(self):
        """
        获取底部导航栏的坐标
        :return:
        """
        bottom_pannel = self.d(resourceId="com.tencent.mm:id/cwx")
        if bottom_pannel.exists():
            x, y = bottom_pannel.center()
            self.max_y = (int(y) - 151)
            return x, self.max_y

    def login_get_sms(self, phone) -> bool:
        """
        尝试采用短信方式登录
        :param phone: 手机号
        :return: True/False
        """
        if phone:
            # 输入手机号
            is_phone_finish = self.__try_force_phone_input(phone)
            if is_phone_finish:
                # 登录的下一步按钮点击
                is_next_finish = self.__try_force_next_step()
                if is_next_finish:
                    # 尝试切换为短信登录
                    is_force_sms = self.__try_force_sms()
                    if is_force_sms:
                        # 尝试点击发送短信按钮
                        is_send_sms_finish = self.__try_send_sms()
                        if is_send_sms_finish:
                            # 尝试点击对话框确认发送短信提醒
                            return self.__try_click_send_sms_ok()
        return False

    def __try_force_phone_input(self, phone, try_nums=5) -> bool:
        """
        输入手机号
        :param phone: 手机号
        :param try_nums: 重试次数
        :return: True/False
        """
        element = self.d(resourceId="com.tencent.mm:id/bfl", text="请填写手机号")
        if element.exists():
            element.click()
            sleep(.5)
            self.d.send_keys(phone)
            sleep(1)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            sleep(1)
            return self.__try_force_phone_input(phone)

    def __try_force_next_step(self, try_nums=5) -> bool:
        """
        登录的下一步按钮点击
        :param try_nums: 尝试次数
        :return:
        """
        next_step_element = self.d(resourceId="com.tencent.mm:id/e09", text="下一步")
        if next_step_element.exists():
            next_step_element.click()
            sleep(2)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            sleep(1)
            return self.__try_force_next_step()

    def __try_force_sms(self, try_nums=5) -> bool:
        """
        尝试切换为短信登录
        :param try_nums: 尝试次数
        :return: True/False
        """
        sms_button_elemnt = self.d(resourceId="com.tencent.mm:id/d35", text="用短信验证码登录")
        if sms_button_elemnt.exists():
            sms_button_elemnt.click()
            sleep(.5)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            sleep(1)
            return self.__try_force_sms()

    def __try_send_sms(self, try_nums=5) -> bool:
        """
        尝试点击发送短信按钮
        :param try_nums: 尝试次数
        :return: True/False
        """
        send_sms_button_element = self.d(resourceId="com.tencent.mm:id/f9_", text="获取验证码")
        if send_sms_button_element.exists():
            send_sms_button_element.click()
            sleep(1)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            return self.__try_send_sms()

    def __try_click_send_sms_ok(self, try_nums=5):
        """
        尝试点击对话框确认发送短信提醒
        :param try_nums: 重试次数
        :return: True/False
        """
        alert_element = self.d(resourceId="com.tencent.mm:id/dm3", text="确定")
        if alert_element.exists():
            alert_element.click()
            sleep(1)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            sleep(1)
            return self.__try_click_send_sms_ok()

    def login_input_sms(self, sms) -> bool:
        """
        输入短信，确认登录
        :param sms: 短信
        :return:
        """
        if sms:
            # 尝试输入短信
            is_sms_input_finish = self.__try_input_sms(sms)
            if is_sms_input_finish:
                # 尝试点击登录按钮进行登录
                is_login = self.__try_click_login_button()
                if is_login:
                    # 尝试检查短信错误提示框
                    return not self.__try_force_sms_error_alert()
        return False

    def __try_input_sms(self, sms, try_nums=5) -> bool:
        """
        尝试输入短信
        :param sms:短信
        :param try_nums:重试次数
        :return: True/False
        """
        sms_input_element = self.d(resourceId="com.tencent.mm:id/bfl", text="请填写验证码")
        if sms_input_element.exists():
            sms_input_element.click()
            sleep(.5)
            self.d.send_keys(sms)
            sleep(.5)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            return self.__try_input_sms(sms)

    def __try_click_login_button(self, try_nums=5) -> bool:
        """
        尝试点击登录按钮进行登录
        :param try_nums: 重试次数
        :return: True/False
        """
        login_button_element = self.d(resourceId="com.tencent.mm:id/e09", text="登录")
        if login_button_element.exists():
            login_button_element.click()
            sleep(1)
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            return self.__try_click_login_button()

    def __try_force_sms_error_alert(self, try_nums=3):
        """
        尝试检查短信错误提示框
        :param try_nums: 重试次数
        :return: True/False
        """
        error_alert_element = self.d(resourceId="com.tencent.mm:id/jh")
        if error_alert_element.exists():
            self.d(resourceId="com.tencent.mm:id/dm3").click()
            sleep(.5)
            self.d(resourceId="com.tencent.mm:id/dm").click()
            logger.error("短信验证错误，返回上一页")
            return True
        else:
            if try_nums <= 0:
                return False
            try_nums -= 1
            sleep(.5)
            return self.__try_force_sms_error_alert()


if __name__ == '__main__':
    wechat = Wechat("192.168.0.23")
    # wechat.init_wx()
    # wechat.test()
    # wechat.unlock()
    # wechat.app_start()
    # wechat.get_contact_info()
    # wechat.get_groups()
    # wechat.get_myself_info()
    # wechat.search_contact("立心")
    # wechat.open_search_result("立心")
    # wechat.send_msg("这个是什么？")
    # wechat.batch_send_msg("进一步测", ["立坤", "AAA . 立心", "小鹏", "伯融"])
    # wechat.batch_send_msg_by_search("""晚点和伯融一起聊下？""", ["AAA . 立心", "立坤"])
    # wechat.login_get_sms("15565063321")
    # wechat.login_input_sms("345567")
    wechat.batch_send_msg_by_keyword("""现货抢购

KN95 封边机
KN95 点焊机
KN95 鼻梁机

全部现货，工厂直销可视频可看货可现场试机
不含税不含发票诚意需要的请联系


电话咨询 18703830130 
微信咨询 18589077222（勿打电话给此号）""", "口罩", ["一家人", "口罩机销售"])
