import request
import ujson
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
http_log = log.getLogger("HTTP POST")

url = "http://httpbin.org/post"
data = {"key1": "value1", "key2": "value2", "key3": "value3"}

# POST请求
response = request.post(url, data=ujson.dumps(data))   # 发送HTTP POST请求
http_log.info(response.json())