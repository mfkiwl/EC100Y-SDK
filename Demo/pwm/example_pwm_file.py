# PWM使用示例

from misc import PWM

'''
* 参数1：PWM号
        注：EC100YCN平台，支持PWM0~PWM5，对应引脚如下：
        PWM0 – 引脚号19
        PWM1 – 引脚号18
        PWM2 – 引脚号16
        PWM3 – 引脚号17
        PWM4 – 引脚号23
        PWM5 – 引脚号22
        
        注：EC600SCN平台，支持PWM0~PWM5，对应引脚如下：
        PWM0 – 引脚号52
        PWM1 – 引脚号53
        PWM2 – 引脚号57
        PWM3 – 引脚号56
        PWM4 – 引脚号70
        PWM5 – 引脚号69
* 参数2：high_time 
        高电平时间，单位ms
* 参数3：cycle_time 
        pwm整个周期时间，单位ms
'''
# 需要配合外设或者使用杜邦线短接对应引脚测试

pwm = PWM(PWM.PWM4, 100, 200)  # 初始化一个pwm对象

pwm.open()  # 开启PWM输出
pwm.close()  # 关闭pwm输出