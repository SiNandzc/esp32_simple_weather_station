from machine import Pin

class Led_Controller:
    leds=None
    net_set=False
    
    #初始化引脚并置为0
    def __init__(self) -> None:
        leds=[16,17,18,19,23,5,2,22]
        self.leds=list(Pin(i,Pin.OUT) for i in leds)
        for i in self.leds:
            i.off()
    
    #led控制函数
    def set_leds(self,led_set='set',net_set=False):
        self.net_set=net_set#设置网络控制标识
        if led_set=='set':
            return
        # 将十进制数转换为二进制并控制led灯
        if led_set>255:
            led_set=255
        elif led_set<0:
            led_set=0
        led_set=bin(led_set).lstrip('0b')
        led_set='0'*(8-len(led_set))+led_set
        p=0
        for i in led_set:
            self.leds[p].value(int(i))
            p+=1 
    
    #获取网络控制标志位
    def get_isset(self):
        return self.net_set