import request
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
http_log = log.getLogger("HTTP GET")

url = "http://httpbin.org/get"

response = request.get(url)   # 发起http GET请求
http_log.info(response.json())   # 以json方式读取返回
