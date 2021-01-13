'''
@Author: Baron
@Date: 2020-04-24
@LastEditTime: 2020-04-24 17:06:08
@Description: example for module umqtt
@FilePath: example_mqtt_file.py
'''
from umqtt import MQTTClient
import utime
import log
import net

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
mqtt_log = log.getLogger("MQTT")

# 判断注网状态
net_sta = net.getState()
if net_sta == -1 and net_sta[1][0] != 1:
    raise OSError("The network is abnormal, please confirm whether the network is connected normally first!")

state = 0

def sub_cb(topic, msg):
    global state
    mqtt_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state = 1

# 创建一个mqtt实例
c = MQTTClient("umqtt_client", "mq.tongxinmao.com", 18830)
# 设置消息回调
c.set_callback(sub_cb)
#建立连接
c.connect()
# 订阅主题
c.subscribe(b"/public/TEST/quecpython")
mqtt_log.info("Connected to mq.tongxinmao.com, subscribed to /public/TEST/quecpython topic" )
# 发布消息
c.publish(b"/public/TEST/quecpython", b"my name is Quecpython!")
mqtt_log.info("Publish topic: /public/TEST/quecpython, msg: my name is Quecpython")

while True:
	c.wait_msg()  # 阻塞函数，监听消息
	if state == 1:
		break

# 关闭连接	
c.disconnect()