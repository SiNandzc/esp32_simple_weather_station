import dht
from machine import Pin

class DHT11_Manager:
    d=None

    #初始化引脚
    def __init__(self):
        self.d=dht.DHT11(Pin(33))

    #获取温度失败返回？？
    def get_temperature(self):
        temperature="??"
        try:
            self.d.measure()
            temperature=self.d.temperature()
        except BaseException as e:
            pass
        return temperature

    #获取湿度失败返回？？
    def get_humidity(self):
        humidity="??"
        try:
            self.d.measure()
            humidity=self.d.humidity()
        except BaseException as e:
            pass
        return humidity
