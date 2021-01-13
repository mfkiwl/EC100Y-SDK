# UART使用

import _thread
import utime
import log
from machine import UART

'''
 * 参数1：端口 
        注：EC100YCN平台与EC600SCN平台，UARTn作用如下
        UART0 - DEBUG PORT
        UART1 – BT PORT
        UART2 – MAIN PORT   
        UART3 – USB CDC PORT
 * 参数2：波特率
 * 参数3：data bits  （5~8）
 * 参数4：Parity  （0：NONE  1：EVEN  2：ODD）
 * 参数5：stop bits （1~2）
 * 参数6：flow control （0: FC_NONE  1：FC_HW）
'''
# 测试该示例代码需要配置uart

# 设置日志输出级别
log.basicConfig(level=log.INFO)
uart_log = log.getLogger("UART")

state = 1


def uartWrite():
    count = 10
    # 配置uart
    uart = UART(UART.UART1, 115200, 8, 0, 1, 0)
    while count:
        write_msg = "Hello count={}".format(count)
        # 发送数据
        uart.write(write_msg)
        uart_log.info("Write msg :{}".format(write_msg))
        utime.sleep(1)
        count -= 1
    uart_log.info("uartWrite end!")


def UartRead():
    global state
    uart = UART(UART.UART1, 115200, 8, 0, 1, 0)
    while 1:
        # 返回是否有可读取的数据长度
        msgLen = uart.any()
        # 当有数据时进行读取
        if msgLen:
            msg = uart.read(msgLen)
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            # str
            uart_log.info("UartRead msg: {}".format(utf8_msg))
        else:
            continue
    state = 0


def run():
    # 创建一个线程来监听接收uart消息
    _thread.start_new_thread(UartRead, ())


if __name__ == "__main__":
    uartWrite()
    run()
    while 1:
        if state:
            pass
        else:
            break

# 运行结果示例
'''
INFO:UART:Write msg :Hello count=8
INFO:UART:Write msg :Hello count=7
INFO:UART:Write msg :Hello count=6
INFO:UART:Write msg :Hello count=5
INFO:UART:Write msg :Hello count=4
INFO:UART:Write msg :Hello count=3
INFO:UART:Write msg :Hello count=2
INFO:UART:Write msg :Hello count=1
INFO:UART:uartWrite end!
INFO:UART:UartRead msg: read msg 1

INFO:UART:UartRead msg: read msg 2

INFO:UART:UartRead msg: read msg 3
'''
