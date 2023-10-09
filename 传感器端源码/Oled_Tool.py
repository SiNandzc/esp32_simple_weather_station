from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep
##在多次实验中oled硬件常常不可靠
##为了保证整个系统的工作正常，该模块所有方法均有异常捕获，保证在oled出错时仍能上传数据

class OLED_Manager:
    OLED = None
    

    #初始化oled并绘制启动画面
    def __init__(self):
        try:
            i2c = I2C(sda=Pin(13), scl=Pin(14))
            self.OLED = SSD1306_I2C(128, 64, i2c)
            self.OLED.fill(1)
            self.OLED.show()
            self.OLED.fill(0)
            self.OLED.show()
            self.OLED.text("IOT System", 25, 8, 2)
            self.OLED.text("Welcome!", 35, 28, 2)
            self.OLED.show()
            sleep(1)
        except BaseException as e:
            return

    # 绘制工作界面
    def working(self, t=0, i=0, h=0, net="No"):
        try:
            self.OLED.fill(0)
            self.OLED.show()
            self.OLED.text("Work", 45, 8, 2)
            self.OLED.text("Temp: " + str(t) + "C", 5, 18, 2)
            self.OLED.text("RH: " + str(h) + "%", 5, 28, 2)
            self.OLED.text("net_status", 5, 38, 2)
            self.OLED.text(net, 5, 48, 2)
            self.OLED.show()
        except BaseException as e:
            return


    # 绘制设置界面
    def setting(self,name='',psw='',alter=-1,char=''):
        try:
            self.OLED.fill(0)
            self.OLED.show()
            self.OLED.text("Set_WIFI", 32, 8, 2)
            self.OLED.text("Name", 5, 18, 2)
            if alter!=0:
                self.OLED.text(name, 5, 28, 2)
            self.OLED.text("PassWord ", 5, 38, 2)
            self.OLED.text('*'*len(psw), 5, 48, 2)
            self.OLED.show()
            sleep(0.1)
            # 绘制闪烁效果
            if alter==0:
                self.OLED.text("Name<--", 5, 18, 2)
                self.OLED.text(name, 5, 28, 2)
                self.OLED.show()
            if alter==1:
                self.OLED.text("PassWord<--", 5, 38, 2)
                self.OLED.text('*'*len(psw)+char, 5, 48, 2)
                self.OLED.show()
        except BaseException as e:
            return

