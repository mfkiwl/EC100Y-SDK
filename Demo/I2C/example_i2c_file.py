import log
from machine import I2C

'''
I2C使用示例
'''

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
i2c_log = log.getLogger("I2C")

I2C_SLAVE_ADDR = 0x1B  # i2c 设备地址 
WHO_AM_I= bytearray({0x02, 0})   # i2c 寄存器地址，以buff的方式传入，取第一个值，计算一个值的长度

data = bytearray({0x12, 0})   # 输入对应指令
i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)  # 返回i2c对象
i2c_obj.write(I2C_SLAVE_ADDR, WHO_AM_I, 1, data, 2) # 写入data

r_data = bytearray(2)  # 创建长度为2的字节数组接收
i2c_obj.read(I2C_SLAVE_ADDR, WHO_AM_I, 1, r_data, 2, 0)   # read
i2c_log.info(r_data[0])  
i2c_log.info(r_data[1])

