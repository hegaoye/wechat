# coding=utf-8

from time import sleep

import uiautomator2 as u2


class FaceBook:
    def __init__(self):
        self.d = u2.connect('192.168.0.28')

    def app_start(self):
        self.d(text="Facebook").click()

    def share_life(self, text):
        self.d(className="android.view.ViewGroup", descriptionContains='发帖').click()
        sleep(.5)
        self.d.xpath('//android.widget.ScrollView/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
        sleep(.5)
        self.d.send_keys(text)
        sleep(1)
        self.d.click(0.919, 0.083)

    def add_new_friend(self):
        l = self.d(className="android.view.ViewGroup", descriptionContains='加为朋友')
        l[0].click()
        sleep(1)
        self.add_new_friend()

    def choose_friend_tab(self):
        sleep(1)
        self.d.xpath(
            '//android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]').click()

    def confirm_friend(self):
        l = self.d(className="android.view.ViewGroup", descriptionContains='确认')
        print(len(l))
        l[0].click()
        sleep(1)
        self.confirm_friend()

    def thumbs_up(self):
        l = self.d(className="android.widget.TextView", descriptionStartsWith='赞按钮，双击')
        if not l[0].exists():
            self.d(scrollable=True).scroll.vert.forward(steps=100)
        else:
            l[0].click()
            sleep(1)
        self.thumbs_up()

    def test(self):
        # self.d(scrollable=True).scroll.vert.forward(steps=200)
        self.d(scrollable=True).scroll.toEnd()
        sleep(.5)
        # self.test()

    def messager_open_one(self, text):
        self.d.xpath(
            '//*[@resource-id="android:id/content"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[4]').click()

        sleep(1)
        input_text = self.d(className="android.widget.EditText", text="Aa")
        input_text.click()
        sleep(.2)
        self.d.send_keys(text)
        sleep(1)
        self.d.xpath(
            '//android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[4]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]').click()
        sleep(1)
        self.d.press("back")


if __name__ == '__main__':
    facebook = FaceBook()
    facebook.d.press("home")
    facebook.app_start()
    facebook.thumbs_up()
    # facebook.choose_friend_tab()
    # facebook.add_new_friend()
    # facebook.confirm_friend()
    # facebook.share_life("this my second day use facebook")
    # facebook.messager_open_one("hello")
