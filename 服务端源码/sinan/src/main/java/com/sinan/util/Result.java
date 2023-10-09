package com.sinan.util;

import com.sinan.pojo.Record;
import lombok.Data;

import java.util.*;

/*结果工具类
* 用于服务层记录打包，控制层网络传输*/
@Data
public class Result {
    Integer code;
    String msg;
    List<Collection<Object>> data=new ArrayList<>();

    /**
     * 打包成功查询到的数据并加工去掉年月日信息
     * @param data 记录
     * @return 对象本身
     */
    public static Result successResult(List<Record> data){
        Result result = new Result();
        result.code=202;
        result.msg="Success";
        for (Record datum : data) {
            Collection<Object> i = new ArrayList<>();
            i.add(datum.getDateTime().getHour()+":"+datum.getDateTime().getMinute()+":"+datum.getDateTime().getSecond());
            i.add(datum.getTemperature());
            i.add(datum.getHumidity());
            result.data.add(i);
        }
        return result;
    }

    /**
     * 打包成功查询到的数据保留年月日信息
     * @param data 记录
     * @return 对象本身
     */
    public static Result successOriginalResult(List<Record> data){
        Result result = new Result();
        result.code=202;
        result.msg="Success";
        for (Record datum : data) {
            Collection<Object> i = new ArrayList<>();
            i.add(datum.getDateTime());
            i.add(datum.getTemperature());
            i.add(datum.getHumidity());
            result.data.add(i);
        }
        return result;
    }

    /**
     * 返回查询失败结果
     * @return 无数据的对象本身
     */
    public static Result failResult(){
        Result result = new Result();
        result.code=202;
        result.msg="Fail";
        return result;
    }
}
