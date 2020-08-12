# domoticz-mqtt2gardena
Python script to status, battery and connectivity data from Gardena using MQTT to Domoticz (or any other MQTT) 
Tested this on Gardena Sileno City, but should work on all Gardena/Husqvarna mowers

# Config
- [Setup Domoticz with MQTT server](https://www.domoticz.com/wiki/MQTT)
- [Install Python3 on your Domoticz server](https://www.domoticz.com/wiki/Using_Python_plugins)
- [Install paho.mqtt to your Python libraries](http://www.steves-internet-guide.com/into-mqtt-python-client/)
- [Create account for Gardena API and generate API Key](https://developer.husqvarnagroup.cloud/)
- Create 3 dummy devices in Domoticz (Battery: Percentage, Connectivity: Percentage and State: Text)
-- Battery: Percentage (DOMOTICZ_MOWER_RFLINK_IDX)
-- Status: Text (DOMOTICZ_MOWER_STATUS_IDX)
-- Connectivity: Percentage (DOMOTICZ_MOWER_RFLINK_IDX)
- Edit the gardena.py and edit the variables listed, make sure the MQTT is pointing to the right IP (default: Localhost). 
- Run the script: ```  python3 gardena.py```
- Check if the dummy devices receive the correct values, if not, make sure your variables are all set correctly. 

# Auto startup
- To run the script in the background by default, install it using [PM2](https://pm2.keymetrics.io/).

# TODO:
- I also made a script to start and stop the mower, will add this later to this repo.
