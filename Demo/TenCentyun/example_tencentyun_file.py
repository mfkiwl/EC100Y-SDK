from TenCentYun import TXyun
import log
import net

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
txyun_log = log.getLogger("TenCentYun")

'''
腾讯云物联网套件客户端功能
'''

# 判断注网状态
net_sta = net.getState()
if net_sta == -1 and net_sta[1][0] != 1:
    raise OSError("The network is abnormal, please confirm whether the network is connected normally first!")

productID = ""  # 产品标识（参照接入腾讯云应用开发指导）
devicename = ""   # 设备名称（参照接入腾讯云应用开发指导）
devicePsk = ""   # 设备密钥（一型一密认证此参数传入None， 参照接入腾讯云应用开发指导）
ProductSecret = None   # 产品密钥（一机一密认证此参数传入None，参照接入腾讯云应用开发指导）

tenxun = TXyun(productID, devicename, devicePsk, ProductSecret)  # 创建连接对象
state = 5

def sub_cb(topic, msg):   # 云端消息响应回调函数
    global state
    txyun_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state -=1

tenxun.setMqtt()  # 设置mqtt
tenxun.setCallback(sub_cb)   # 设置消息回调函数
topic = ""  # 输入自定义的Topic
tenxun.subscribe(topic)   # 订阅Topic
tenxun.start()
tenxun.publish(topic, "hello world")   # 发布消息

while 1:
    if state:
        pass
    else:
        break