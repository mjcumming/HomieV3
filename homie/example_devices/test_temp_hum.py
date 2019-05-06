#!/usr/bin/env python

import time

from homie.device_temperature_humidity import Device_Temperature_Humidity

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


try:

    dimmer = Device_Temperature_Humidity(name = 'Temp Hum',mqtt_settings=mqtt_settings)
    
    while True:
        dimmer.update(50,10)
        time.sleep(5)
        dimmer.update(10,30)
        time.sleep(5)
        dimmer.update(90,90)
        time.sleep(5)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")        
