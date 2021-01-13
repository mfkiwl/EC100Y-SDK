'''
@Author: Baron
@Date: 2020-04-24
@LastEditTime: 2020-04-26 09:56:08
@Description: example for module usocket
@FilePath: example_socket_file.py
'''
# 导入usocket模块
import usocket
import log
import net

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
socket_log = log.getLogger("SOCKET")


# 判断注网状态
net_sta = net.getState()
if net_sta == -1 and net_sta[1][0] != 1:
    raise OSError("The network is abnormal, please confirm whether the network is connected normally first!")

# 创建一个socket实例
sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
# 解析域名
sockaddr=usocket.getaddrinfo('www.tongxinmao.com',80)[0][-1]
# 建立连接
sock.connect(sockaddr)
# 向服务端发送消息
ret=sock.send('GET /News HTTP/1.1\r\nHost: www.tongxinmao.com\r\nAccept-Encoding: deflate\r\nConnection: keep-alive\r\n\r\n')
socket_log.info('send %d bytes' % ret)
#接收服务端消息
data=sock.recv(256)
socket_log.info('recv %s bytes:' % len(data))
socket_log.info(data.decode())

# 关闭连接
sock.close()
	