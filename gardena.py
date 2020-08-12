import websocket
from threading import Thread
import time
import sys
import requests
import json
import paho.mqtt.client as mqtt

# account specific values
USERNAME = 'USERNAME_GARDENA'
PASSWORD = 'PASSWORD_GARDENA'
API_KEY = 'API_KEY_GARDENA'

# other constants
AUTHENTICATION_HOST = 'https://api.authentication.husqvarnagroup.dev'
SMART_HOST = 'https://api.smart.gardena.dev'

#MQTT
DOMOTICZ_TOPIC = 'domoticz/in'
DOMOTICZ_MOWER_STATUS_IDX = 0  #STATUS IDX DOMOTICZ
DOMOTICZ_MOWER_BATTERY_IDX = 1  #BATTERY IDX DOMOTICZ
DOMOTICZ_MOWER_RFLINK_IDX = 2 #CONNECTIVITY IDX DOMOTICZ
DOMOTICZ_MQTT = 'localhost'
DOMOTICZ_MQTT_PORT = 1883

mqtt_client = mqtt.Client()
mqtt_client.connect(DOMOTICZ_MQTT,DOMOTICZ_MQTT_PORT,60)
mqtt_client.loop_start()

class Client:
    def on_message(self, message):
        print("msg", message)        
        mqtt_parse(message)
        sys.stdout.flush()

    def on_error(self, error):
        print("error", error)

    def on_close(self):
        self.live = False
        print("### closed ###")
        sys.exit(0)

    def on_open(self):
        print("### connected ###")

        self.live = True

        def run(*args):
            while self.live:
                time.sleep(1)

        Thread(target=run).start()

def mqtt_parse(message):
    response = json.loads(message)
    response_type = response['type']

    # Types are DEVICE, LOCATION, COMMON and MOWER
    if response_type == 'MOWER': 
        mqtt_client.publish(DOMOTICZ_TOPIC, json.dumps({'idx': DOMOTICZ_MOWER_STATUS_IDX, 'svalue': response['attributes']['activity']['value']}))
    elif response_type == 'COMMON':
        mqtt_client.publish(DOMOTICZ_TOPIC, json.dumps({'idx': DOMOTICZ_MOWER_BATTERY_IDX, 'svalue': '{}%'.format(response['attributes']['batteryLevel']['value'])}))
        mqtt_client.publish(DOMOTICZ_TOPIC, json.dumps({'idx': DOMOTICZ_MOWER_RFLINK_IDX, 'svalue':  '{}%'.format(response['attributes']['rfLinkLevel']['value'])}))

if __name__ == "__main__":
    payload = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD,
               'client_id': API_KEY}

    print("Logging into authentication system...")
    r = requests.post('{}/v1/oauth2/token'.format(AUTHENTICATION_HOST), data=payload)
    assert r.status_code == 200, r
    auth_token = r.json()["access_token"]

    headers = {
        "Content-Type": "application/vnd.api+json",
        "x-api-key": API_KEY,
        "Authorization-Provider": "husqvarna",
        "Authorization": "Bearer " + auth_token
    }

    r = requests.get('{}/v1/locations'.format(SMART_HOST), headers=headers)
    assert r.status_code == 200, r
    assert len(r.json()["data"]) > 0, 'location missing - user has not setup system'
    location_id = r.json()["data"][0]["id"]

    payload = {
        "data": {
            "type": "WEBSOCKET",
            "attributes": {
                "locationId": location_id
            },
            "id": "does-not-matter"
        }
    }
    print("Logged in (%s), getting WebSocket ID..." % auth_token)
    r = requests.post('{}/v1/websocket'.format(SMART_HOST), json=payload, headers=headers)

    assert r.status_code == 201, r
    print("WebSocket ID obtained, connecting...")
    response = r.json()
    websocket_url = response["data"]["attributes"]["url"]

    # websocket.enableTrace(True)
    client = Client()
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=client.on_message,
        on_error=client.on_error,
        on_close=client.on_close)
    ws.on_open = client.on_open
    ws.run_forever(ping_interval=150, ping_timeout=1)
