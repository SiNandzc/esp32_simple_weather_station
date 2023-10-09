package com.sinan.controller;

import com.sinan.service.WebService;
import com.sinan.util.Result;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.ToString;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
/*控制层*/
@RestController
public class WebController {

    @Autowired
    private WebService webService;

    /**
     * 获取最新数据
     * @return 结果对象
     */
    @GetMapping("/getNew")
    public Result getAll(){
        return webService.getNew();
    }

    /**
     * 获取指定日期的数据
     * @param date 指定日期（yyyy-MM-dd）
     * @return 结果对象
     */
    @GetMapping("/getByDate")
    public Result getByDate(@RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd")LocalDate date){
        return webService.getByDate(date);
    }

    /**
     * 查询指定的日期，可忽略部分数据
     * @param date 日期数据json格式，部分数据为空
     * @return 结果对象
     */
    @PostMapping("/getByParams")
    public Result postData(@RequestBody Mydate date){
        return webService.getByParam(date.getYear(), date.getMonth(), date.getDay());
    }
}


@Data
@ToString
@AllArgsConstructor
/**
 * 接收日期数据对象
 */
class Mydate{

    public Integer year;
    public Integer month;
    public Integer day;
}