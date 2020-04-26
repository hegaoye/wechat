import os
from time import sleep


class ArtOfWar:
    def __init__(self, device_id):
        self.device_id = str(device_id)

    def open_fire(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 540 2000")

    def play_ad(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 360 1500")

    def back(self):
        self.run_cammand("adb -s "+ self.device_id+" shell  input keyevent 4")

    def close_ad(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 950 450")

    def sand(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 800 1200")

    def snow(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 800 1600")

    def open_fire_jimmy(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 540 1900")

    def play_ad_jimmy(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 360 1500")

    def back_jimmy(self):
        self.run_cammand("adb -s "+ self.device_id+" shell  input keyevent 4")

    def close_ad_jimmy(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 950 450")

    def sand_jimmy(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 800 1100")

    def snow_jimmy(self):
        self.run_cammand("adb -s  "+ self.device_id+"  shell input tap 800 1700")

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
            sleep(32)
            self.play_ad()
            sleep(32)
            self.back()
            sleep(.5)
            # self.close_ad()
            # sleep(.2)

    def run_jimmy(self):
        '''
        自动执行
        :return:
        '''
        while True:
            self.open_fire_jimmy()
            sleep(.5)
            self.open_fire_jimmy()
            sleep(32)
            self.play_ad_jimmy()
            sleep(32)
            self.back_jimmy()
            sleep(.5)
            # self.close_ad_jimmy()
            # sleep(.2)

    def run_sand(self):
        while True:
            self.sand()
            sleep(.5)
            self.open_fire()
            sleep(10)
            self.play_ad()
            sleep(32)
            self.back()
            sleep(.5)

    def run_snow(self):
        while True:
            self.snow()
            sleep(.5)
            self.open_fire()
            sleep(15)
            self.play_ad()
            sleep(32)
            self.back()
            sleep(.5)

    def run_sand_jimmy(self):
        while True:
            self.sand_jimmy()
            sleep(.5)
            self.open_fire_jimmy()
            sleep(10)
            self.play_ad_jimmy()
            sleep(32)
            self.back_jimmy()
            sleep(.5)

    def run_snow_jimmy(self):
        while True:
            self.sand_jimmy()
            sleep(.5)
            self.open_fire_jimmy()
            sleep(15)
            self.play_ad_jimmy()
            sleep(32)
            self.back_jimmy()
            sleep(.5)
