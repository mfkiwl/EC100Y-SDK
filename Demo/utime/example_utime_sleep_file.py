'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_sleep_file.py
'''
import utime
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
time_log = log.getLogger("Sleep")

for i in [0,1,2,3,4,5]:
    utime.sleep(1)   # 休眠(单位 m)
    time_log.info(i)

for i in [0,1,2,3,4,5]:
    utime.sleep_ms(1000)   # 休眠(单位 ms)
    time_log.info(i)
