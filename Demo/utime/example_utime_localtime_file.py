'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_loacltime_file.py
'''
import utime
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
time_log = log.getLogger("LocalTime")

# 获取本地时间，返回元组
tupe_t = utime.localtime()

time_log.info(tupe_t)