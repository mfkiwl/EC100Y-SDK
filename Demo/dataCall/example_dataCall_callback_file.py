import dataCall
import net
import utime

'''
dataCall.setCallback()
用户回调函数，当网络状态发生变化，比如断线、上线时，会通过该回调函数通知用户。
'''


state = 5

# 定义回调函数
def nw_cb(args):
    global state
    pdp = args[0]   # pdp索引
    nw_sta = args[1]  # 网络连接状态 0未连接， 1已连接
    if nw_sta == 1:
        print("*** network %d connected! ***" % pdp)
    else:
        print("*** network %d not connected! ***" % pdp)
    state -=1

# 注册回调函数
dataCall.setCallback(nw_cb)

# 进入飞行模式模拟触发
net.setModemFun(4)

utime.sleep(2)

# 退出飞行模式再次模拟触发回调
net.setModemFun(1)

while 1:
    if state:
        pass
    else:
        break
