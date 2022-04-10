import json
import signal
import time as t
from  mqtt import MyAIMqttClient
from classifier import RFClassifier
from queue import Queue


in_service = True

def exit_gracefully(signum, frame):
    global in_service
    in_service = False
signal.signal(signal.SIGINT, exit_gracefully)

def data_formatter(msg):
    # CO2,AQI,PM2.5,PM10,Rain,Smoke
    return [[int(msg["CO2"]),0,0,0,0,0]]

def run():
    global in_service
    msg_queue = Queue()
    cls = RFClassifier()
    clt = MyAIMqttClient(msg_queue)
    while in_service:
        if not msg_queue.empty():
            msg = msg_queue.get()
            res = cls.inference(data_formatter(msg))[0]
            clt.publish(res)
        t.sleep(0.5)
    clt.disconnect()

if __name__ == '__main__':
    run()