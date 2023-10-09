package com.sinan.util;

import com.sinan.controller.ListenSense;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

/*服务启动时启功传感器监听*/
@Component
public class ThreadStarter implements ApplicationListener<ContextRefreshedEvent> {

    @Autowired
    private ListenSense listenSense;

    /**
     * 启动监听线程
     * @param event spring启动完成事件
     */
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        Thread thread = new Thread(listenSense);
        thread.start();
    }
}





