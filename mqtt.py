import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import config
import functools

def callback(msg_queue, client, userdata, message):
    message = json.loads(message.payload)
    msg_queue.put(message)

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
