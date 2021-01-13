'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module ntptime
@FilePath: example_ntptime_file.py
'''
import ntptime
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
ntp_log = log.getLogger("NtpTime")

# 查看默认ntp服务
ntp_log.info(ntptime.host)
# 设置ntp服务
ntptime.sethost('pool.ntp.org')

# 同步ntp服务时间
ntptime.settime()