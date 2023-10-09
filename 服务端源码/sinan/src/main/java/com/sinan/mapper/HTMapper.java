package com.sinan.mapper;

import com.sinan.pojo.Record;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.time.LocalDate;
import java.util.List;

/*持久层*/
@Mapper
public interface HTMapper {

    /**
     * 查询最新数据
     * @return 记录列表
     */
    @Select("select * from h_t_table where (select max(dateTime) from h_t_table)=dateTime limit 1")
    List<Record> selectNew();

    /**
     * 查询指定日期数据
     * @param date 日期
     * @return 记录列表
     */
    @Select("select * from h_t_table where date (dateTime)=#{date} order by dateTime ")
    List<Record> selectByDate(@Param("date") LocalDate date);

    /**
     * 上传数据到数据库
     * @param temperature 温度
     * @param humidity 湿度
     */
    @Update("insert into h_t_table value(now(),#{temperature},#{humidity})")
    void update(@Param("temperature")int temperature,@Param("humidity") int humidity);

    /**
     * 查询按部分日期信息
     * @param year 年
     * @param month 月
     * @param day 日
     * @return 记录列表
     */
    List<Record> getByParam(@Param("year")Integer year,@Param("month") Integer month,@Param("day") Integer day);
}
