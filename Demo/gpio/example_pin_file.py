# Pin使用示例

from machine import Pin

'''
* 参数1：引脚号
        EC100YCN平台引脚对应关系如下：
        GPIO1 – 引脚号22
        GPIO2 – 引脚号23
        GPIO3 – 引脚号178
        GPIO4 – 引脚号199
        GPIO5 – 引脚号204
        
        EC600SCN平台引脚对应关系如下：
        GPIO1 – 引脚号10
        GPIO2 – 引脚号11
        GPIO3 – 引脚号12
        GPIO4 – 引脚号13
        GPIO5 – 引脚号14
        GPIO6 – 引脚号15
        GPIO7 – 引脚号16
        GPIO8 – 引脚号39
        GPIO9 – 引脚号40
        GPIO10 – 引脚号48
* 参数2：direction 
        IN – 输入模式
        OUT – 输出模式
* 参数3：pull
        PULL_DISABLE – 禁用模式
        PULL_PU – 上拉模式
        PULL_PD – 下拉模式
* 参数4：level  
        0 设置引脚为低电平
        1 设置引脚为高电平
'''
gpio1 = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)

gpio1.write(1) # 设置gpio1 输出
gpio1.read() # 获取gpio的当前高低状态
# >>> 1