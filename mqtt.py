import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import config
import functools
import time

def callback(msg_queue, client, userdata, message):
    message = json.loads(message.payload)
    name = message["sensor_name"]
    co2_ppm = 0
    if name == "CO2":
        max_v = 5000
        co2_ppm = int(message["co2"])
        co2_ppm = min(co2_ppm, max_v)
        co2_ppm = (co2_ppm/max_v)*100
        if co2_ppm ==0: return
        msg_queue.put(co2_ppm)


class MyAIMqttClient:
    def __init__(self, msg_queue):
        self.client_id = config.CLIENT_ID # What is the purpose of ClientID?
        self.msg_queue = msg_queue
        self.init_client()

    def init_client(self):
        self.client = AWSIoTPyMQTT.AWSIoTMQTTClient(self.client_id)
        self.client.configureEndpoint(config.ENDPOINT, 8883)
        self.client.configureCredentials(config.PATH_TO_AMAZON_ROOT_CA_1, config.PATH_TO_PRIVATE_KEY, config.PATH_TO_CERTIFICATE)
        self.client.connect()
        self.client.subscribe(config.SUB_TOPIC, 1, functools.partial(callback, self.msg_queue))

    def publish(self, message):
        message = {
            "message": str(message)
        }
        self.client.publish(config.TOPIC, json.dumps(message), 1) 
        print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")


    def disconnect(self):
        self.client.disconnect()
