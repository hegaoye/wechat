import os
from time import sleep


class ArtOfWar:
    def __init__(self):
        pass

    def open_fire(self):
        self.run_cammand("adb -s  S2D7N19328004812  shell input tap 540 2000")

    def play_ad(self):
        self.run_cammand("adb -s  S2D7N19328004812  shell input tap 360 1500")

    def back(self):
        self.run_cammand("adb -s S2D7N19328004812 shell  input keyevent 4")

    def open_fire_jimmy(self):
        self.run_cammand("adb -s  RELBB18A19500825  shell input tap 540 1900")

    def play_ad_jimmy(self):
        self.run_cammand("adb -s  RELBB18A19500825  shell input tap 360 1500")

    def back_jimmy(self):
        self.run_cammand("adb -s RELBB18A19500825 shell  input keyevent 4")

    def run_cammand(self, cammand):
        os.system(cammand)

    def run(self):
        '''
        自动执行
        :return:
        '''
        while True:
            self.open_fire()
            sleep(.5)
            self.open_fire()
            sleep(25)
            self.play_ad()
            sleep(33)
            self.back()
            sleep(1)

    def run_jimmy(self):
        '''
        自动执行
        :return:
        '''
        while True:
            self.open_fire_jimmy()
            sleep(.5)
            self.open_fire_jimmy()
            sleep(25)
            self.play_ad_jimmy()
            sleep(33)
            self.back_jimmy()
            sleep(1)
