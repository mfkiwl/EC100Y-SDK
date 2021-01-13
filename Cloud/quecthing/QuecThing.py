import uhashlib
import ubinascii
import request
import modem

def run():
    productKey = "K3I5ZkgyZjkydGli"
    productSecret = "VUFyVE92YVJmSUNQ"
    rand = "q9f5UdAlh687grFl0JVuyY6095302ehd"
    imei = modem.getDevImei()
    VER = '1'

    h1 = uhashlib.md5()
    h1.update(imei + "," + productSecret + "," + rand)
    SIGN = ubinascii.hexlify(h1.digest()).decode()
    print("MD5:   %s" % SIGN)  # 8ab41bc1e5e74fbf9cec16a6e0990d89

    DATA = imei + ";" + rand + ";" + SIGN
    print("DATA:  %s  " %DATA)
    h1 = uhashlib.sha1(productSecret)
    res = ubinascii.hexlify(h1.digest()).decode()
    print(res)
    res = uhashlib.hash_sha1(res, 20)
    print("SHA1(PS) :  %s" % res)
    aes_key = res[0:16].upper()
    print("aes_key : %s" % aes_key)
    res = uhashlib.aes_ecb(aes_key, DATA)
    print(res)
    raw = uhashlib.hash_base64(res)
    print(raw)
    data = productKey + ";" + raw + ";" + VER
    url = "220.180.239.212:8415"
    # url = "192.168.25.64:30884"
    response = request.post(url, data=data)
    print(response.json())   # 获取到密钥
    # {'RESPCODE': 10200, 'RESPMSG': 'SUCCESS', 'SERVERURI': 'mqtt://220.180.239.212:8420', 'DS': 'd5f01bddfc994c037be90ede69399ac0'}
    return response.json()

if __name__ == '__main__':
    pw = run()

    ds = pw.get("DS")

    def sub_cb(topic, msg):
        # global state
        # mqtt_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
        # state = 1
        print("Subscribe Recv:   %s, %s" %(topic.decode(), msg.decode()))

    def mqtt():
        from umqtt_v2 import MQTTClient
        # IMEI+”_”+VER
        imei = modem.getDevImei()
        clientid = "{}_1".format(imei)
        pw = ds
        c = MQTTClient(clientid, "220.180.239.212", 8420, clientid, pw)
        c.set_callback(sub_cb)
        c.connect()

        sub_topic = "quec/{imei}/down"
        pub_topic = "quec/{imei}/up"
        c.subscribe(sub_topic)