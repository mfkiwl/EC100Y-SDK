import request
import log

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
http_log = log.getLogger("HTTP SSL")
# https请求
url = "https://myssl.com"

response = request.get(url)  # 支持ssl
http_log.info(response.text)