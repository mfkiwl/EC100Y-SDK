import ure
import net
import math
import utime
import _thread
import modem
from machine import Timer
from umqtt import MQTTClient
from machine import UART
from machine import I2C
from machine import Pin

TEMPERATUR = None  # 温度
HUMIDITY = None  # 湿度
LIGHT = None  # 光照
GPSMSG = []  # gps数据


class GetDeviceInfo():
    '''
    温湿度，GPS数据采集
    '''

    def __init__(self):
        self.uart = UART(UART.UART2, 9600, 8, 0, 1, 0)
        self.w_data = bytearray({0, 0})
        self.r_data = bytearray(2)

        self.I2C_SLAVE_ADDR_HDC1080 = 0x40
        self.HDC1080_TEMPERATURE = 0x00
        self.HDC1080_HUMIDITY = 0x01
        self.HDC1080_CONFIGURATION = 0x02
        self.HDC1080_MANUFACTURER_ID = 0xFE
        self.HDC1080_DEVICE_ID = 0xFF
        self.I2C_SLAVE_ADDR_BH1750 = 0x23
        self.BH1750_POWER_ON = 0x01
        self.BH1750_H_RE_MODE = 0x10

        self.gpio5 = Pin(Pin.GPIO5, Pin.OUT, Pin.PULL_DISABLE, 1)
        self.gpio5.write(0)
        self.i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        reg_addr = bytearray({0x02, 0})
        self.i2c_obj.write(self.I2C_SLAVE_ADDR_HDC1080, reg_addr, 1, self.w_data, 2)
        utime.sleep_ms(10)

    def middle(self):
        global TEMPERATUR
        global HUMIDITY
        global LIGHT
        global GPSMSG

        while True:
            reg_addr = bytearray({0xFE, 0xFE})
            self.i2c_obj.read(self.I2C_SLAVE_ADDR_HDC1080, reg_addr, 1, self.r_data, 2, 0)
            utime.sleep_ms(10)
            reg_addr = bytearray({0xFF, 0xFF})
            self.i2c_obj.read(self.I2C_SLAVE_ADDR_HDC1080, reg_addr, 1, self.r_data, 2, 0)
            utime.sleep_ms(10)

            reg_addr = bytearray({0x00, 0x00})
            ret = self.i2c_obj.read(self.I2C_SLAVE_ADDR_HDC1080, reg_addr, 1, self.r_data, 2, 10)
            if ret == 0:
                TEMPERATUR = ((self.r_data[0] * 256 + self.r_data[1]) / (2 ** 16)) * 165 - 40
            print('T', TEMPERATUR)
            utime.sleep_ms(10)

            reg_addr = bytearray({0x01, 0x01})
            ret = self.i2c_obj.read(self.I2C_SLAVE_ADDR_HDC1080, reg_addr, 1, self.r_data, 2, 10)
            if ret == 0:
                HUMIDITY = ((self.r_data[0] * 256 + self.r_data[1]) / (2 ** 16)) * 100
            print('H', HUMIDITY)
            reg_addr = bytearray({0x01, 0x01})
            self.i2c_obj.write(self.I2C_SLAVE_ADDR_BH1750, reg_addr, 1, self.w_data, 0)
            utime.sleep_ms(10)

            reg_addr = bytearray({0x10, 0x10})
            self.i2c_obj.write(self.I2C_SLAVE_ADDR_BH1750, reg_addr, 1, self.w_data, 0)
            utime.sleep_ms(200)

            reg_addr = bytearray({0x00, 0x00})
            ret = self.i2c_obj.read(self.I2C_SLAVE_ADDR_BH1750, reg_addr, 0, self.r_data, 2, 0)
            if ret == 0:
                LIGHT = (self.r_data[0] * 256 + self.r_data[1]) / 1.2
            print('L', LIGHT)
            len = self.uart.any()

            if len > 0:
                buf = self.uart.read(len)
                gps_data = buf.decode().strip("b")
                # print(gps_data)
                try:
                    r = ure.search("GPRMC(.+?)M", gps_data)
                    gps_msg = r.group(0).split(",")
                except Exception as e:
                    continue
                print("GPS", gps_msg)
            utime.sleep(1)

    def run(self):
        _thread.start_new_thread(self.middle, ())


def lng_format(l):
    '''
    经纬度纠偏
    :param l:
    :return:
    '''
    r = str(float(l) / 100)
    d, f = r.split(".")
    a = str(float("0." + f) * 100 / 60)
    res = a.split(".")[1][0:6]
    data = d + res

    lens = len(data)
    if lens < 9:
        if lens == 8:
            data = data + "0"
        elif lens == 7:
            data = data + "00"
        elif lens == 6:
            data = data + "000"
    return int(data)


def lat_format(l):
    '''
    经纬度纠偏
    :param l:
    :return:
    '''
    r = str(float(l) / 100)
    d, f = r.split(".")
    a = str(float("0." + f) * 100 / 60)
    res = a.split(".")[1][0:6]
    data = d + res

    lens = len(data)
    if lens < 8:
        if lens == 7:
            data = data + "0"
        elif lens == 6:
            data = data + "00"
    return int(data)


# gps数据处理
def gpsFormat(data_l):
    # print(data_l)
    try:
        lon = data_l[5]
        lat = data_l[3]
        lon_d = data_l[6]
        lat_d = data_l[4]
        lon = lng_format(lon)  # 31492931
        lat = lat_format(lat)  # 117069201
    except:
        return
    # print(lon, lat)
    if lon_d == "E":
        lon_d = "01"  # 东经
    else:
        lon_d = "02"  # 西经
    if lat_d == "N":
        lat_d = "02"  # 北纬
    else:
        lat_d = "01"  # 南纬
    lon = gpsIntTo16(lon)
    lat = gpsIntTo16(lat)
    print("GPS", lon, lat)
    gps_data = "{}{}{}{}".format(lon_d, lon, lat_d, lat)
    # print(gps_data)
    return gps_data


def gpsIntTo16(n):
    '''
    gps int to 16进制
    '''
    msg = hex(n)[2:]
    msg_len = len(msg)
    if msg_len < 8:
        if msg_len == 7:
            msg = "0" + msg
        elif msg_len == 6:
            msg = "00" + msg
        elif msg_len == 5:
            msg = "000" + msg
    return msg


def NumIntTo16(n):
    '''
    序号 csq int to 16进制
    '''
    if n == 16:
        return "10"
    msg = hex(n).strip("0x")
    if int(msg, 16) != n:
        msg = msg + "0"
    msg_len = len(msg)
    if msg_len < 2:
        msg = "0" + msg
    return msg


def timeIntTo16(n):
    '''
    时间戳转换16进制
    '''
    msg = hex(n).strip("0x")
    while int(msg, 16) != n:
        msg = msg + "0"
    msg_len = len(msg)
    if msg_len < 4:
        if msg_len == 3:
            msg = "0" + msg
        elif msg_len == 2:
            msg = "00" + msg
        elif msg_len == 1:
            msg = "000" + msg
    return msg


def l_IntTo16(n):
    '''
    光照 int to 16进制
    '''
    msg = hex(n).strip("0x")
    while int(msg, 16) != n:
        msg = msg + "0"
    msg_len = len(msg)
    if msg_len < 4:
        if msg_len == 3:
            msg = "0" + msg
        elif msg_len == 2:
            msg = "00" + msg
        elif msg_len == 1:
            msg = "000" + msg
    return msg


def t_h_format(n):
    '''
    温湿度 int To 16进制
    :param n:
    :return:
    '''
    result = math.ceil(n * 100)
    ret = timeIntTo16(result)
    return ret

count = 0
def TrackerMsgFormat(temperature, humidity, light, gps, iccid):
    '''
    上传数据整合，按照要求格式凭接
    :param temperature:
    :param humidity:
    :param light:
    :param gps:
    :return:
    '''
    global count
    if count == 256:
        count = 0
    count += 1
    num = NumIntTo16(count)
    # 当前时间戳
    time_s = timeIntTo16(utime.mktime(utime.localtime()))
    # csq
    csq = NumIntTo16(net.csqQueryPoll())
    # 温度
    t = t_h_format(temperature)
    # 湿度
    h = t_h_format(humidity)
    # 光照
    l = l_IntTo16(math.ceil(light))
    # gps数据
    gps_msg = gpsFormat(gps)

    imei = "3" + "3".join(modem.getDevImei())
    iccid = "3" + "3".join(iccid)
    # 拼接数据包
    TrackerMsgFormat = "fa{num}{time}{imei}004d0110001d{iccid}{csq}fcb000b60000003c200004{TH}220002{l}23001101{gps}00000000000013"
    # 383634343330303130303031303935    3839383631313138323832303039363539343531
    TrackerData = TrackerMsgFormat.format(num=num, time=time_s, imei=imei, iccid=iccid, csq=csq, TH=(t + h), l=l,
                                          gps=gps_msg)
    return TrackerData


class MqttClient():
    '''
    mqtt init
    '''

    def __init__(self, clientid, server, port, pw):
        self.clientid = clientid
        self.pw = pw
        self.server = server
        self.port = port
        self.uasename = clientid
        self.client = None

    def connect(self):
        self.client = MQTTClient(self.clientid, self.server, self.port, self.uasename, self.pw, keepalive=300)
        self.client.set_callback(self.sub_cb)
        self.client.connect()

    def sub_cb(self, topic, msg):
        print("Subscribe Recv:   %s, %s" % (topic.decode(), msg.decode()))

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def publish(self, topic, msg, qos=0):
        self.client.publish(topic, msg, qos)

    def disconnect(self):
        self.disconnect()

    def __loop_forever(self, t):
        # print("loop_forever")
        try:
            self.client.ping()
        except:
            return -1

    def __listen(self):
        while True:
            try:
                self.client.wait_msg()
            except OSError as e:
                return -1

    def start(self):
        _thread.start_new_thread(self.__listen, ())
        t = Timer(1)
        t.start(period=20000, mode=t.PERIODIC, callback=self.__loop_forever)


if __name__ == '__main__':
    print("############### GetDeviceInfo  #############")
    g = GetDeviceInfo()
    g.run()

    # MQTT init
    clientid = "{imei}_1"
    pw = ""
    iccid = ""
    mqttServer = "220.180.239.212"
    c = MqttClient(clientid, mqttServer, 8420, pw)
    c.connect()
    sub_topic = "quec/{imei}/down"
    pub_topic = "quec/{imei}/up"
    c.subscribe(sub_topic)
    c.start()

    while 1:
        utime.sleep(3)
        if (TEMPERATUR != None) and (HUMIDITY != None) and (LIGHT != None) and (GPSMSG != []):
            if GPSMSG[3] != "":
                print("T", TEMPERATUR)
                print("H", HUMIDITY)
                print("L", LIGHT)
                print("G", GPSMSG)
                try:
                    data = TrackerMsgFormat(TEMPERATUR, HUMIDITY, LIGHT, GPSMSG, iccid)
                    c.publish(pub_topic, data)  # 发布到云端
                except:
                    continue
            else:
                print("Get the GPS data")
        else:
            print("Get the GPS data")



