import hmac
import ujson
import utime
import _thread
from umqtt import MQTTClient
import urandom
from hashlib import sha256
from machine import Timer
import uos


MQTT_SERVER = "{}.iot-as-mqtt.cn-shanghai.aliyuncs.com"
S_HMAC = "deviceName{}productKey{}random{}"
HMAC = "clientId{}deviceName{}productKey{}"
CLIENT_ID = "{}|securemode=3,signmethod=hmacsha256|"
CLIENT_ID_R = "{}|securemode=2,authType=register,random={},signmethod=hmacsha256|"

class aLiYun:

    def __init__(self, productKey, productSecret=None, DeviceName=None, DeviceSecret=None):
        self.productKey = productKey
        self.productSecret = productSecret
        self.DeviceName = DeviceName
        self.DeviceSecret = DeviceSecret

        self.callback = self.setCallback
        self.recvCb = None
        self.mqtt_client = None
        self.password = None
        self.port = 1883

        self.clientID = None
        self.username = "{}&{}".format(self.DeviceName, self.productKey)

    def formatConnectInfo(self, secret, randomNum=None):
        secret = secret
        if randomNum != None:
            mqt_id = CLIENT_ID_R.format(self.clientID, randomNum)
            hmac_msg = S_HMAC.format(self.DeviceName, self.productKey, randomNum)
        else:
            mqt_id = CLIENT_ID.format(self.clientID, randomNum)
            hmac_msg = HMAC.format(self.clientID, self.DeviceName, self.productKey)
        return mqt_id, secret, hmac_msg

    def setMqtt(self, clientID=None, clean_session=False, keepAlive=300):
        self.clientID = clientID
        if self.productSecret == None:
            ssl = False
            mqt_id, secret, hmac_msg = self.formatConnectInfo(self.DeviceSecret)
        else:
            if "secret.json" in uos.listdir():
                msg = check_secret(self.DeviceName)
                if msg:
                    self.DeviceSecret = msg
                    mqt_id, secret, hmac_msg = self.formatConnectInfo(self.DeviceSecret)
                    self.mqtt_client = self.connect(mqt_id, secret, hmac_msg, keepAlive, clean_session, ssl=False)
                    print("[INFO] The MQTT connection was successful")
                    return 0
            print("[INFO] MQTT dynamic registration")
            ssl = True
            randomNum = self.rundom()
            mqt_id, secret, hmac_msg = self.formatConnectInfo(self.productSecret, randomNum=randomNum)
            try:
                mqtts_cl = self.connect(mqt_id, secret, hmac_msg, keepAlive, clean_session, ssl)
            except:
                return -1         
            utime.sleep(2)
            mqtts_cl.wait_msg()
            utime.sleep(1)
            mqtts_cl.disconnect()
            return 0
        try:
            self.mqtt_client = self.connect(mqt_id, secret, hmac_msg, keepAlive, clean_session, ssl)
            return 0
        except:
            return -1

    def connect(self, mqt_id, secret, hmac_msg, keepAlive, clean_session, ssl):
        mqt_server = MQTT_SERVER.format(self.productKey)
        self.password = hmac.new(bytes(secret, "utf8"), msg=bytes(hmac_msg, "utf8"), digestmod=sha256).hexdigest()
        mqtt_client = MQTTClient(mqt_id, mqt_server, self.port, self.username, self.password,
                                      keepAlive, ssl=ssl)
        mqtt_client.set_callback(self.proc)
        mqtt_client.connect(clean_session=clean_session)
        return mqtt_client

    def subscribe(self, topic, qos=0):
        try:
            self.mqtt_client.subscribe(topic, qos)
            return 0
        except OSError as e:
            print("[WARNING] subscribe failed. Try to reconnect : %s" % str(e))
            return -1

    def publish(self, topic, msg, retain=False, qos=0):
        try:
            self.mqtt_client.publish(topic, msg, retain, qos)
            return 0
        except OSError as e:
            print("[WARNING] Publish failed. Try to reconnect : %s" % str(e))
            return -1

    def proc(self, topic, msg):
        # print("proc  subscribe recv:")
        # print(topic, msg)
        if str(topic, "utf-8") == "/ext/register":
            data = ujson.loads(msg)
            self.DeviceSecret = data.get("deviceSecret")
            self.productSecret = None
            data = {self.DeviceName: self.DeviceSecret}
            save_Secret(data)         # save DeviceSecret
            self.setMqtt(self.clientID)
        else:
            return self.recvCb(topic, msg)

    def setCallback(self, callback):
        self.recvCb = callback

    '''
    def __loop_forever(self, t):
        # print("loop_forever")
        try:
            self.mqtt_client.ping()
        except:
            return -1
    '''

    def __listen(self):
        while True:
            try:
                self.mqtt_client.wait_msg()
            except OSError as e:
                return -1

    def start(self):
        _thread.start_new_thread(self.__listen, ())
        # t = Timer(1)
        # t.start(period=20000, mode=t.PERIODIC, callback=self.__loop_forever)

    def rundom(self):
        msg = ""
        for i in range(0,5):
            num = urandom.randint(1, 10)
            msg += str(num)
        return msg

def save_Secret(data):
    secret_data = {}
    if "secret.json" in uos.listdir():
        with open("secret.json", "r", encoding="utf-8") as f:
            secret_data = ujson.load(f)
            print(secret_data)
    try:
        with open("secret.json", "w+", encoding="utf-8") as w:
            secret_data.update(data)
            ujson.dump(secret_data, w)
    except Exception as e:
        print("[ERROR] File write failed : %s" % str(e))

def check_secret(deviceName):
    try:
        with open("secret.json", "r", encoding="utf-8") as f:
            secret_data = ujson.load(f)
    except Exception as e:
        print("[ERROR] File Open failed : %s" % str(e))
    device_secret = secret_data.get(deviceName, None)
    if device_secret != None:
        return device_secret
    return False