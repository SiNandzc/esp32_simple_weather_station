
# 时间2023/9/13
# 传感器端主程序代码
# 功能实现：
#1、OLED屏实时显示温湿度数据与网络状态
#2、温湿度报警效果（包括灯光效果、蜂鸣器效果）
#3、响应用户控制界面html文件
#4、前端网页控制led灯与设置温湿度预警数据
#4、WIFI连接手动设置
#5、数据记录上载服务器端


from RGB_Drive import RGB_controller
from time import sleep
from Oled_Tool import OLED_Manager
from time import sleep
from Dht11 import DHT11_Manager
from Buttons import Buttons_Controller
from Net_Tool import Net_Manager
from Led_manager import Led_Controller

# 系统对象
class System_Main:
    led_rgb_control = RGB_controller()#RGB对象
    oled_controller = OLED_Manager()#OLED对象
    dht_manager =  DHT11_Manager()#温湿度传感器对象
    net_manager=Net_Manager()#网络层对象
    buttons_manager = Buttons_Controller(net_manager)#按键对象
    led_controller=Led_Controller()#led灯对象
    Temp = None
    Humidity = None
    Light = None
    net="No connect!"#网络信息属性
    warn = False#警报标志位
    json=None#json配置信息

    def __init__(self):
        pass

    # 扫描数据变化
    def __scan__(self):
        # 如果wifi未连接尝试连接，如果尝试次数过多停止连接尝试
        if not self.net_manager.get_isconnect() and self.net!='later reset!':
            self.net_manager.connect_network()
        # 如果网络层接收到的json数据被改变则更新json到系统控制类
        if self.json!=self.net_manager.get_json():
            self.json=self.net_manager.get_json()
        #如果json数据中有led控制信息则启动控制，True代表正在网络控制标志位
        if self.json["led"]!=None:
            self.led_controller.set_leds(self.json["led"],True)
        else:
            #如果没有则关闭控制，并将网络控制标志位置为False
            self.led_controller.set_leds()
        # 获取网络连接状态
        self.net=self.net_manager.get_connect()
        # 获取温湿度
        self.Temp = self.dht_manager.get_temperature()
        self.Humidity = self.dht_manager.get_humidity()
        # 将网络控制层的温湿度信息更新
        self.net_manager.set_th(self.Temp,self.Humidity)
        #警报状态扫描如果数据为？？代表传感器未检测到数据，则跳过警报状态扫描
        if self.Temp=="??" or self.Humidity=="??":
            return
        # 大于json数据中指定的范围则启动报警
        if self.Temp<self.json["temperatureMin"] or self.Temp>self.json["temperatureMax"] or self.Humidity<self.json["humidityMin"] or self.Humidity>self.json["humidityMax"]:
            self.warn = True
            self.led_controller.set_leds(255)
            self.system_warn()
        else:
            self.warn = False
            if not self.led_controller.get_isset():
                self.led_controller.set_leds(0)

    # 系统工作
    def system_work(self):
        # 如果RGB灯未显示工作状态且不在警报状态则切换到工作状态
        if not self.led_rgb_control.get_key()[0] and not self.warn:
            self.led_rgb_control.run(0)
        # OLE显示传感器及网络信息
        self.oled_controller.working(t=self.Temp, h=self.Humidity, net=self.net)

    #系统设置
    def system_set(self):
        # 如果RGB灯未显示设置状态且不在警报状态则切换到设置状态
        if not self.led_rgb_control.get_key()[1]  and not self.warn:
            self.led_rgb_control.run(1)
        # 如果用户进入设置状态，则显示设置信息
        if self.buttons_manager.get_confirm():
            name, psw = self.buttons_manager.get_name_psw()
            alter = self.buttons_manager.get_alter()
            char=self.buttons_manager.get_char()
            self.oled_controller.setting(name, psw, alter,char)
        else:
            #没有进入设置信息状态，则显示配置信息
            name, psw = self.net_manager.get_name_psw()
            self.oled_controller.setting(name, psw)

    #系统报警
    def system_warn(self):
        # 如果RGB灯未显示警报状态则切换到警报状态
        if not self.led_rgb_control.get_key()[2]:
            self.led_rgb_control.run(2)

    #系统主循环
    def system_main_loop(self):
        while True:
            sleep(0.1)
            self.__scan__()#扫面更新数据
            #获取按键控制层标志进入对应的交互函数
            if self.buttons_manager.get_status() == 0:
                self.system_work()
            elif self.buttons_manager.get_status() == 1:
                self.system_set()
            #清除按键信息
            self.buttons_manager.clear()

if '__main__' == __name__:
    while True:
        Esp32_system = System_Main()
        sleep(2)
        Esp32_system.system_main_loop()

