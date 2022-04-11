import base64
import time
import json


def decoder(data):
    base64_message = data["PayloadData"]
    DeviceId = data["WirelessDeviceId"]
    type_dict = ["CO2","Window","Motion","WaterLeak"]
    # base64_message = 'MDAwMDAwMDA0OTAwMjEwMmU4MDA3NTA2MDAwMA=='
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    decoded_data = []
    for i in range(0, len(message), 4):
        two_byte_string = message[i : i+4]
        two_byte_string = bytes.fromhex(two_byte_string)
        val = int.from_bytes(two_byte_string, "little")
        decoded_data.append(val)


    data_json = {
        "wireless_device_id" : DeviceId,
        "sensor_type" : decoded_data[0],
        "sensor_name" : type_dict[decoded_data[0]],
        "command_id" : decoded_data[1],
        "timepstamp" : decoded_data[2],
        "timepstamp_upload" : time.time()
    }
    sensor_type = decoded_data[0]
    sensor_specific = {
        0: ["humidity", "temperature", "co2", "is_covered"],
        1: ["humidity", "temperature", "is_lockded"],
        2: ["humidity", "temperature", "is_moving"],
        3: ["humidity", "temperature", "is_short"],
    }

    metric_list = sensor_specific[sensor_type]
    for i in range(3, len(decoded_data)):
        metric = metric_list[i-3]
        decoded_data[i] = decoded_data[i]/10 if metric in ["humidity", "temperature"] else decoded_data[i]
        data_json[metric] = decoded_data[i]
    data_str = json.dumps(data_json, indent=4)
    print(data_str)
# decoder("MDAwMDAwMDA0OTAwMjEwMmU4MDA3NTA2MDAwMA==")