import json
import urequests
import network
from time import sleep
from _thread import start_new_thread
try:
    import usocket as socket
except:
    import socket
import gc
gc.collect()

class Net_Manager:
    wlan=network.WLAN(network.STA_IF)
    mysocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_key=False#监听标志位
    net_name = ''#网络名称
    password = ''#密码
    json=None#配置信息
    connect="finding"#连接状态信息
    try_times=0#尝试连接次数
    temp=None#网络层温度数据
    humidity=None#网络层湿度数据
    
    # 初始化网络并加载init.json配置数据
    def __init__(self):
        self.wlan.active(True) 
        self.load_n_p()
        self.mysocket.bind(('', 80))
        self.mysocket.listen(5)
    
    #加载init.json数据
    def load_n_p(self):
        self.try_times=0
        with open("init.json","r")as f:
            self.json=json.loads(f.read())
            self.net_name=self.json['name']
            self.password=self.json['password']
            self.json["led"]=None
            print(self.net_name+':'+self.password)
    
    #连接网络函数
    def connect_network(self):
        self.try_times+=1#连接次数加一
        #连接次数超过30次关闭连接，并将网络状态置为'later reset!'阻止继续尝试，将监听标志位置为false
        if self.try_times>30:
            self.wlan.disconnect()
            self.connect='later reset!'
            self.listen_key=False
            return
        if self.connect=='No find!':#如果未找到网络表明网络连接线程正在运行没必要再次启动该线程，阻止其再次启动
            return
        try:
            #扫描并启动连接
            ssid_all=self.wlan.scan()
            for ssid in ssid_all:
                if self.net_name==str(bytes.decode(ssid[0])):
                    self.connect='find!'
                    if self.password=='':
                        self.wlan.connect(self.net_name)
                    else:
                        self.wlan.connect(self.net_name,self.password)
                    sleep(3)
                    time=15
                    while not self.wlan.isconnected() and time>0:
                        sleep(1)
                        time-=1
                    return
            self.connect='No find!'
        except BaseException as e:
            self.connect='No find!'
            self.listen_key=False


    #监听请求
    def listen_socket(self):
        while self.listen_key:
            while True:
                try:
                    conn, addr = self.mysocket.accept()
                    request = conn.recv(1024)
                    request = str(request)
                    conn.send('HTTP/1.1 200 OK\n')
                    data=''
                    #响应温湿度请求
                    if '/get_th' in request:
                        conn.send('Content-Type: text/json\n')
                        conn.send('Connection: close\n\n')
                        data={"temperature":str(self.temp),"humidity":str(self.humidity)}
                        conn.sendall('\r\n\r\n'+json.dumps(data))
                    #接收处理设置信息请求
                    elif '/update' in request:
                        data=request.split("/update?")[1]
                        data=data.split(" HTTP/1.1")[0]
                        data=data.split('&')
                        data_dict={"led":[]}
                        for i in data:
                            if i.split('=')[0]=='led':
                                data_dict['led'].append(i.split('=')[1])
                            else:
                                if i.split('=')[1]!='':
                                    data_dict[i.split('=')[0]]=int(i.split('=')[1])
                                else:
                                    data_dict[i.split('=')[0]]='none'
                        if  isinstance(data_dict["h_max"],int):
                            self.json["humidityMax"]=data_dict["h_max"]
                        if isinstance(data_dict["h_min"],int):
                            self.json["humidityMin"]=data_dict["h_min"]
                        if isinstance(data_dict["t_max"],int):
                            self.json["temperatureMax"]=data_dict["t_max"]
                        if isinstance(data_dict["t_min"],int):
                            self.json["temperatureMin"]=data_dict["t_min"]
                        # 保存json配置数据
                        self.save_init()
                        led=0
                        if data_dict["led"]!=[]:
                            for i in data_dict["led"]:
                                led+=pow(2,7-int(i))
                        self.json["led"]=led
                    else:
                        #返回html控制界面文件
                        conn.send('Content-Type: text/html\n')
                        conn.send('Connection: close\n\n')
                        with open('control_platform.html','r')as f:
                            for line in f:
                                data=line
                                conn.sendall('\r\n\r\n'+data)
                        conn.sendall('\r\n\r\n'+data)
                    conn.close()
                except BaseException as e:
                    break
        self.json['led']=None
        
    #循环上传数据
    def updateToServer(self):
        while self.listen_key:
            # 创建UDP套接字
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 目标服务器的IP地址和端口
            server_ip = self.json["IP"]
            server_port = 45678
            while True:
                # 要发送的 JSON 数据
                data = {"temperature": self.temp, "humidity": self.humidity}
                if not isinstance(data["temperature"],int) or not isinstance(data["humidity"],int):
                    sleep(2)
                    continue
                json_data = json.dumps(data)  # 将 JSON 对象转换为字符串
                try:
                    # 发送UDP消息
                    udp_socket.sendto(json_data.encode(), (server_ip, server_port))
                    print("JSON数据已发送")
                except Exception as e:
                    print("发送UDP消息时发生错误:", e)
                    break
                sleep(2)

    #保存配置
    def save_init(self,name=True,psw=True):
        if name!=True:
            self.json['name']=name
        if psw!=True:
            self.json['password']=psw
        with open("init.json",'w')as f:
            f.write(json.dumps(self.json))
        self.load_n_p()
        if name!=True or psw!=True:
            self.connect='fonding'
            self.listen_key=False
            self.wlan.disconnect()
            self.connect_network()
    
    #返回状态并启动监听和数据上传
    def get_connect(self):
        if self.wlan.isconnected():
            self.connect=self.wlan.ifconfig()[0]
            if not self.listen_key:
                self.listen_key=True
                start_new_thread(self.listen_socket,())
                start_new_thread(self.updateToServer,())
        else:
            self.listen_key=False
        return self.connect
    
    #返回扫描到的WiFi
    def get_around_wifi(self):
        ssid_all=self.wlan.scan()
        return list(str(bytes.decode(ssid[0])) for ssid in ssid_all)
    
    #返回是否连接到网络
    def get_isconnect(self):
        return self.wlan.isconnected()
    
    # 获取配置中的wifi名称和密码
    def get_name_psw(self):
        return self.net_name, self.password
    
    #获取配置信息
    def get_json(self):
        return self.json
    
    # 设置网络层的温湿度数据
    def set_th(self,t,h):
        self.temp=t
        self.humidity=h