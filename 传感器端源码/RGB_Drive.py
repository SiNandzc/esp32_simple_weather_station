import time
import neopixel
from _thread import start_new_thread
from machine import Pin, PWM

# 彩灯对象
class RGB_controller:
    buzzer_pin = Pin(0, Pin.OUT)
    RGB = neopixel.NeoPixel(Pin(15), 4)
    key = [False, False, False]
    R = 0
    G = 0
    B = 0

    # 初始化RGB
    def __init__(self):
        for i in range(4):
            self.RGB[i] = (0, 10, 0)
        self.RGB.write()

    # 设置RGB颜色亮度等数据
    def __setColor(self, led, value):
        self.RGB[led] = value
        self.RGB.write()

    # 启动RGB效果线程
    def run(self, status):
        if status == 0:
            self.key = [True, False, False]
            start_new_thread(self.working, ())
        elif status == 1:
            self.key = [False, True, False]
            start_new_thread(self.setting, ())
        elif status == 2:
            self.key = [False, False, True]
            start_new_thread(self.warning, ())

    # RGB工作效果
    def working(self):
        while self.key[0]:
            for i in range(4):
                self.RGB[i % 4] = (0, 0, 10)
                self.RGB[(i + 1) % 4] = (0, 10, 0)
                self.RGB[(i + 2) % 4] = (0, 10, 0)
                self.RGB[(i + 3) % 4] = (0, 10, 0)
                self.RGB.write()
                time.sleep(1)

    # RGB设置效果
    def setting(self):
        while self.key[1]:
            for i in range(4):
                self.__setColor(i, (0, 0, 20))
            time.sleep(1)
            for i in range(4):
                self.__setColor(i, (0, 20, 0))
            time.sleep(1)

    # RGB警报效果
    def warning(self):
        buzzer_pwm = PWM(self.buzzer_pin)
        note_freq = 880 
        note_duration = 500
        buzzer_pwm.freq(note_freq)
        while self.key[2]:
            buzzer_pwm.duty(800)
            for i in range(4):
                self.__setColor(i, (0, 0, 250))
            time.sleep(1)
            buzzer_pwm.duty(0)
            for i in range(4):
                self.__setColor(i, (250, 0, 0))
            time.sleep(1)
        buzzer_pwm.deinit()

    #获取RGB状态
    def get_key(self):
        return self.key