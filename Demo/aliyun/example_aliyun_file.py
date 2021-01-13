'''
@Author: Pawn
@Date: 2020-09-28
@Description: example for module aLiYun
@FilePath: example_aliyun_file.py
'''
import log
import net
from aLiYun import aLiYun

# 设置日志输出级别
log.basicConfig(level=log.INFO)
aliYun_log = log.getLogger("ALiYun")

# 判断注网状态
net_sta = net.getState()
if net_sta == -1 and net_sta[1][0] != 1:
    raise OSError("The network is abnormal, please confirm whether the network is connected normally first!")

productKey = ""  # 产品标识(参照阿里云应用开发指导)
productSecret = None  # 产品密钥（使用一机一密认证时此参数传入None，参照阿里云应用开发指导)
DeviceName = ""  # 设备名称(参照阿里云应用开发指导)
DeviceSecret = ""  # 设备密钥（使用一型一密认证此参数传入None，免预注册暂不支持，需先在云端创建设备，参照阿里云应用开发指导)

# 创建aliyun连接对象
ali = aLiYun(productKey, productSecret, DeviceName, DeviceSecret)

# 设置mqtt连接属性
clientID = ""  # 自定义字符（不超过64）
ali.setMqtt(clientID, clean_session=False, keepAlive=300)

state = 5


# 回调函数
def sub_cb(topic, msg):
    global state
    aliYun_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state -= 1


# 设置回调函数
ali.setCallback(sub_cb)
topic = ""  # 云端自定义或自拥有的Topic
# 订阅主题
ali.subscribe(topic)
# 发布消息
ali.publish(topic, "hello world")
# 运行
ali.start()

while 1:
    if state:
        pass
    else:
        break







