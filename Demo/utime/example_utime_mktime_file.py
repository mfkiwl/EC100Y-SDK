'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_mktime_file.py
'''
import utime
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
time_log = log.getLogger("MkTime")

# 返回当前时间戳，参数为元组
t = utime.mktime(utime.localtime())

time_log.info(t)