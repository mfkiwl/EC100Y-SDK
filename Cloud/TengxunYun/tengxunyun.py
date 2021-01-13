import utime
import urandom
import hmac
import hashlib
import base64
import _thread
import hmacSha1
import ucryptolib
import request
import ujson
import uos
from machine import Timer
from umqtt import MQTTClient


class TXyun:

    def __init__(self, productID, devicename, devicePsk, ProductSecret=None):

        self.productID = productID
        self.devicename = devicename
        self.devicePsk = devicePsk
        self.ProductSecret = ProductSecret

        self.mqtt_server = "{}.iotcloud.tencentdevices.com".format(productID)
        self.username = None
        self.password = None
        # 生成 MQTT 的 clientid 部分, 格式为 ${productid}${devicename}
        self.clientid = "{}{}".format(productID, devicename)

        self.mqtt_client = None
        self.callback = self.setCallback
        self.recvCb = None
        self.url = "http://ap-guangzhou.gateway.tencentdevices.com/register/dev"
        
    def setMqtt(self, clean_session=False, keepAlive=300):
        if self.ProductSecret != None:
            self.DynamicConnectInfo()
            try:
                self.mqtt_client = self.connect(keepAlive, clean_session)
                return 0
            except:
                return -1
        else:
            try:
                self.mqtt_client = self.connect(keepAlive, clean_session)
                return 0
            except:
                return -1

    def connect(self, keepAlive, clean_session):
        self.formatConnectInfo()
        mqtt_client = MQTTClient(self.clientid, self.mqtt_server, 1883, self.username, self.password,keepAlive)
        mqtt_client.connect(clean_session=clean_session)
        mqtt_client.set_callback(self.proc)
        return mqtt_client

    def proc(self, topic, msg):
        return self.recvCb(topic, msg)

    def formatConnectInfo(self):
        expiry = int(utime.mktime(utime.localtime())) + 60 * 60
        connid = self.rundom()

        self.username = "{};12010126;{};{}".format(self.clientid, connid, expiry)
        try:
            token = hmac.new(base64.b64decode(self.devicePsk), msg=bytes(self.username, "utf8"),
                         digestmod=hashlib.sha256).hexdigest()
        except:
            raise ("Key generation exception!Please check the device properties")
        self.password = "{};{}".format(token, "hmacsha256")


    def DynamicConnectInfo(self):
        numTime = utime.mktime(utime.localtime())
        nonce = self.rundom()
        msg = "deviceName={}&nonce={}&productId={}&timestamp={}".format(self.devicename, nonce, self.productID ,numTime)
        hmacInfo = hmacSha1.hmac_sha1(self.ProductSecret, msg)
        base64_msg = base64.b64encode(bytes(hmacInfo, "utf8"))

        data = {
            "deviceName": self.devicename,
            "nonce": nonce,
            "productId": self.productID,
            "timestamp": numTime,
            "signature": base64_msg.decode()
        }

        data_json = ujson.dumps(data)

        response = request.post(self.url, data=data_json)
        res_raw = response.json()

        code = res_raw.get("code")
        if code == 1021:
            print("Device has been activated!")
            if "tx_secret.json" in uos.listdir():
                msg = check_secret(self.devicename)
                if msg:
                    self.devicePsk = msg
                    self.formatConnectInfo()
                    return 0
            else:
                print("The device is active, but the key file tx_secret.json is missing.")
                return -1
        payload = res_raw.get("payload")
        mode = ucryptolib.MODE_CBC
        raw = base64.b64decode(payload)
        key = self.ProductSecret[0:16].encode()
        iv = b"0000000000000000"
        cryptos = ucryptolib.aes(key, mode, iv)
        plain_text = cryptos.decrypt(raw)
        data = plain_text.decode().split("\x00")[0]
        self.devicePsk = ujson.loads(data).get("psk")
        data = {self.devicename: self.devicePsk}
        save_Secret(data)
        self.formatConnectInfo()

    def setCallback(self, callback):
        self.recvCb = callback

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
            except OSError:
                return -1

    def start(self):
        _thread.start_new_thread(self.__listen, ())
        # t = Timer(1)
        # t.start(period=20000, mode=t.PERIODIC, callback=self.__loop_forever)

    def rundom(self):
        msg = ""
        for i in range(0, 5):
            num = urandom.randint(1, 10)
            msg += str(num)
        return int(msg)


def save_Secret(data):
    secret_data = {}
    if "tx_secret.json" in uos.listdir():
        with open("tx_secret.json", "r", encoding="utf-8") as f:
            secret_data = ujson.load(f)
            print(secret_data)
    try:
        with open("tx_secret.json", "w+", encoding="utf-8") as w:
            secret_data.update(data)
            ujson.dump(secret_data, w)
    except Exception as e:
        print("[ERROR] File write failed : %s" % str(e))


def check_secret(deviceName):
    try:
        with open("tx_secret.json", "r", encoding="utf-8") as f:
            secret_data = ujson.load(f)
    except Exception as e:
        print("[ERROR] File Open failed : %s" % str(e))
    device_secret = secret_data.get(deviceName, None)
    if device_secret != None:
        return device_secret
    return False