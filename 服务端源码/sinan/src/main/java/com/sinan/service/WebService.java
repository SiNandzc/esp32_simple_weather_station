package com.sinan.service;

import com.sinan.mapper.HTMapper;
import com.sinan.pojo.Record;
import com.sinan.util.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.util.List;

/*服务层*/
@Service
public class WebService {

    @Autowired
    private HTMapper htMapper;

    /**
     * 获取最新数据
     * @return 结果对象
     */
    public Result getNew(){
        List<Record> records = htMapper.selectNew();
        return Result.successResult(records);
    }

    /**
     * 获取指定日期数据
     * @return 结果对象
     */
    public Result getByDate(LocalDate date){
        List<Record> records = htMapper.selectByDate(date);
        return Result.successResult(records);
    }

    /**
     * 获取指定部分日期数据
     * @return 结果对象
     */
    public Result getByParam(Integer year,Integer month,Integer day){
        if (year==null&&month==null&&day==null){
            return Result.failResult();
        }
        List<Record> records = htMapper.getByParam(year, month, day);
        return Result.successOriginalResult(records);
    }

    /**
     * 上传传感器信息
     * @param temperature 温度
     * @param humidity 湿度
     */
    public void update(int temperature, int humidity) {
        htMapper.update(temperature,humidity);
    }
}
