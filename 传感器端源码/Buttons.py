from machine import Pin
from time import sleep_ms


class Buttons_Controller:
    net_manager=None#网络层对象
    net_name = ''#WiFi名
    password = ''#WiFi密码
    status = 0#当前展示状态0为系统工作1为系统设置
    pinButtons = None#存储引脚对象
    confirm = False#是否进入设置状态
    char = 48#密码待输入字符
    alter = 0#当前设置状态0为设置WiFi名中，1为设置WiFi密码中
    befor=None#存储按键信息
    p_wifi=0#当前WIFI名在列表中的地址
    wifi_name_list=["None"]#扫描到的WiFi名列表

    def __init__(self,net_m):
        # 初始化网络层对象和按键引脚
        self.net_manager=net_m
        buttons = [32, 25, 26, 4]
        self.pinButtons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in buttons]
        #初始化引脚
        self.setup_interrupt_handlers()
        
    #消抖
    def debounce(self, handler):
        def wrapped_handler(pin):
            sleep_ms(80)  # 等待一段时间以消除按键的抖动效应
            handler(pin)
        return wrapped_handler

    #按键1处理
    def button1_interrupt_handler(self, pin):
        if self.befor==1:
            return
        self.befor=1
        # 如果设置为进入设置状态，系统就在设置信息和工作信息间切换
        if not self.confirm:
            self.status += 1
            self.status %= 2
        else:
            # 如果当前为设置状态则初始化配置json数据并重启网络，并清除按键对象存储的名称密码信息，退出设置状态
            self.net_manager.save_init(self.net_name,self.password)
            # 清楚名称密码
            self.net_name=''
            self.password=''
            # 设置状态置为False
            self.confirm = False

    #按键2处理
    def button2_interrupt_handler(self, pin):
        if self.befor==2:
            return
        self.befor=2
        #如果当前不是设置状态则进入设置状态，并将密码位指向0，并获取周围WiFi名称储存，将当前WiFi名指向第一个WiFi名
        if not self.confirm:
            self.confirm = True
            self.p_wifi=0
            wifis=self.net_manager.get_around_wifi()
            if len(wifis)>0:
                self.wifi_name_list=wifis
            self.net_name=self.wifi_name_list[0]
        # 如果当前正在设置名称则切换到设置密码，反之亦然
        elif self.confirm and self.alter == 0:
            self.alter = 1
        elif self.confirm and self.alter == 1:
            self.char=48
            self.alter = 0

    #按键3处理
    def button3_interrupt_handler(self, pin):
        if self.befor==3:
            return
        self.befor=3
        if self.confirm:
            # 如果当前为设置状态且正在设置wifi名，将wifi地址指向下一个并更新wifi名称属性
            if self.alter == 0:
                self.p_wifi-=1
                if self.p_wifi<0:
                    self.p_wifi=len(self.wifi_name_list)-1
                self.net_name=self.wifi_name_list[self.p_wifi]
            # 如果当前为设置状态且正在设置密码，将当前的待输入字符添加至密码属性末尾，并重置待输入字符置为48
            if self.alter == 1:
                self.password += chr(self.char)
            self.char=48

    #按键4处理
    def button4_interrupt_handler(self, pin):
        if self.befor==4:
            return
        self.befor=4
        # 如果当前为设置状态且正在设置wifi名，将wifi地址指向上一个并更新wifi名称属性
        if self.confirm and self.alter==0:
            self.p_wifi+=1
            self.p_wifi%=len(self.wifi_name_list)
            self.net_name=self.wifi_name_list[self.p_wifi]
        # 如果当前为设置状态且正在设置密码，将当前的待输入字符加1，且限制在48~122
        elif self.confirm and self.alter==1:
            self.char += 1
            self.char %= 123
            if self.char == 0:
                self.char = 48
    
    #初始化引脚
    def setup_interrupt_handlers(self):
        self.pinButtons[0].irq(trigger=Pin.IRQ_FALLING, handler=self.debounce(self.button1_interrupt_handler))
        self.pinButtons[1].irq(trigger=Pin.IRQ_FALLING, handler=self.debounce(self.button2_interrupt_handler))
        self.pinButtons[2].irq(trigger=Pin.IRQ_FALLING, handler=self.debounce(self.button3_interrupt_handler))
        self.pinButtons[3].irq(trigger=Pin.IRQ_FALLING, handler=self.debounce(self.button4_interrupt_handler))

    #清除上一次的按键事件信息
    def clear(self):
        self.befor=None

    # 获取当前状态
    def get_status(self):
        return self.status

    #获取当前设置状态
    def get_alter(self):
        return self.alter

    #获取wifi名密码
    def get_name_psw(self):
        return self.net_name, self.password

    # 获取当前是否正在设置状态
    def get_confirm(self):
        return self.confirm

    # 获取待输入字符
    def get_char(self):
        return chr(self.char)