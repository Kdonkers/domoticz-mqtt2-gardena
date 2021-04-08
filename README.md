# domoticz-mqtt2-gardena
Python script to status, battery and connectivity data from Gardena using MQTT to Domoticz (or any other MQTT) 
Tested this on Gardena Sileno City, but should work on all Gardena/Husqvarna mowers

# Configuration for Gardena/Husqvarna mower data 
* [Setup Domoticz with MQTT server](https://www.domoticz.com/wiki/MQTT)
* [Install Python3 on your Domoticz server](https://www.domoticz.com/wiki/Using_Python_plugins)
* [Create account for Gardena API and generate API Key](https://developer.husqvarnagroup.cloud/)
* Create 3 dummy devices in Domoticz:
  * Battery: Percentage (DOMOTICZ_MOWER_RFLINK_IDX)
  * Status: Text (DOMOTICZ_MOWER_STATUS_IDX)
  * Connectivity: Percentage (DOMOTICZ_MOWER_RFLINK_IDX)
* Edit the gardena.py and edit the variables listed, make sure the MQTT is pointing to the right IP (default: Localhost). 
* Run the script:  ``` python3 gardena.py```
* Check if the dummy devices receive the correct values, if not, make sure your variables are all set correctly. 

# Configuration for Gardena mower control
* [Setup Domoticz with MQTT server](https://www.domoticz.com/wiki/MQTT)
* [Install Python3 on your Domoticz server](https://www.domoticz.com/wiki/Using_Python_plugins)
* Create folder 'gardena' in ``` /home/pi/domoticz/scripts ```
* Copy ``` mower_control.sh ``` and ``` mower_control.py ```in the created folder
* Create 3 dummy devices in Domoticz:
    *   Single button: Start mowing
    *   Single button: Park until next operation
    *   Single button: Park until further notice
* Edit the button action in Domoticz with On/Off action  ```  script://gardena/mower_control.sh "INSERT ACTION KEY HERE" ``` 
    * Fill in the action key based on button (for example: ```  script://gardena/mower_control.sh "START_DONT_OVERRIDE" ```):    
        * START_SECONDS_TO_OVERRIDE - Manual operation, use 'seconds' attribute to define duration.
        * START_DONT_OVERRIDE - Automatic operation.
        * PARK_UNTIL_NEXT_TASK - Cancel the current operation and return to charging station.
        * PARK_UNTIL_FURTHER_NOTICE - Cancel the current operation, return to charging station, ignore schedule.

# Auto startup
To run the script in the background by default, install it using [PM2](https://pm2.keymetrics.io/).

