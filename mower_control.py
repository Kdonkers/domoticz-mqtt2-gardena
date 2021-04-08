from threading import Thread
import time
import sys
import requests
import json

# account specific values
USERNAME = 'USERNAME_GARDENA'
PASSWORD = 'PASSWORD_GARDENA'
API_KEY = 'API_KEY_GARDENA'

# other constants
AUTHENTICATION_HOST = 'https://api.authentication.husqvarnagroup.dev'
SMART_HOST = 'https://api.smart.gardena.dev'

# action options for mower
# START_SECONDS_TO_OVERRIDE - Manual operation, use 'seconds' attribute to define duration.
# START_DONT_OVERRIDE - Automatic operation.
# PARK_UNTIL_NEXT_TASK - Cancel the current operation and return to charging station.
# PARK_UNTIL_FURTHER_NOTICE - Cancel the current operation, return to charging station, ignore schedule.
DEVICE_ACTION = sys.argv[1]

def action_mower(mower, action):
    payload = {
        "data": {
            "type": "MOWER_CONTROL",
            "attributes": {
                "command": action
            },
            "id": "does-not-matter"
        } 
    }
    r = requests.put('{}/v1/command/{}'.format(SMART_HOST, device['id']), json=payload, headers=headers)
    assert r.status_code == 202, r
    print("Command {} excecuted...".format(action))
    response = r.json()
    print(response)

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

    r = requests.get('{}/v1/locations/{}'.format(SMART_HOST, location_id), headers=headers)
    assert r.status_code == 200, r
    assert len(r.json()["included"][0]['relationships']['services']['data']) > 0, 'no devices setup'
    devices = r.json()["included"][0]['relationships']['services']['data']

    for device in devices: 
        if(device['type'] == "MOWER"):
            payload = {
                "data": {
                    "type": "MOWER_CONTROL",
                    "attributes": {
                        "command": DEVICE_ACTION
                    },
                    "id": "does-not-matter"
                } 
            }
            r = requests.put('{}/v1/command/{}'.format(SMART_HOST, device['id']), json=payload, headers=headers)
            assert r.status_code == 202, r
            print("Command {} excecuted...".format(DEVICE_ACTION))
