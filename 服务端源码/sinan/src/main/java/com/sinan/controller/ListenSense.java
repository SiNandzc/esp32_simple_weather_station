package com.sinan.controller;

import com.alibaba.fastjson.JSON;
import com.sinan.service.WebService;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RestController;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.HashMap;


@Component
public class ListenSense implements Runnable {

    @Autowired
    WebService webService;

    /*监听传感器UDP信息*/
    @SneakyThrows
    @Override
    public void run() {
        // 指定UDP监听端口
        int port = 45678;
        // 创建UDP套接字并绑定到指定端口
        DatagramSocket socket = new DatagramSocket(port);
        System.out.println("UDP服务器已启动，监听端口 " + port);
        while (true) {
            try {
                // 创建一个字节数组用于接收数据
                byte[] receiveData = new byte[1024];
                // 创建一个数据包对象来接收数据
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                // 接收UDP数据包
                socket.receive(receivePacket);
                // 从数据包中提取接收到的数据
                String receivedMessage = new String(receivePacket.getData(), 0, receivePacket.getLength());
                //解析收到字符串转为json数据
                HashMap hashMap = JSON.parseObject(receivedMessage, HashMap.class);
                //上传数据到数据库
                webService.update((int)hashMap.get("temperature"),(int)hashMap.get("humidity"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
