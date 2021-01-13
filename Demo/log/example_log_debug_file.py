import log

log.basicConfig(level=log.DEBUG)   # 设置日志输出级别

# 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象
log = log.getLogger("debug")

log.debug("Test debug message!!")  
