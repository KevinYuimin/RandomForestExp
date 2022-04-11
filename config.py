import os
ENDPOINT = os.environ.get('AWS_ENDPOINT')
PATH_TO_CERTIFICATE = "certs/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs/AmazonRootCA1.pem"
TOPIC = "ai/prediction"
SUB_TOPIC = "project/sensor/observed/json"
CLIENT_ID = "kevhsu_test"

if not ENDPOINT:
    raise ValueError("AWS IOT ENDPOINT Not Specified")