/*
 * 时间2023/9/20
 * 服务器端代码
 * 功能实现：
 * 响应浏览器页面请求
 * 响应温湿度数据请求
 * 响应查询请求
 * 接收传感器数据上载
 * 数据持久化存储
 */

package com.sinan;

import com.sinan.controller.ListenSense;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SinanApplication {

    /**
     * spring启动入口
     * @param args 参数
     */
    public static void main(String[] args) {
        SpringApplication.run(SinanApplication.class, args);
    }

}
