package com.sinan.pojo;


import lombok.*;
import java.time.LocalDateTime;

/*
* 记录接收对象，用于接收数据库查询到的数据
* */
@AllArgsConstructor
@NoArgsConstructor
@Data
public class Record {
    LocalDateTime dateTime;
    Short temperature;
    Short humidity;
}
