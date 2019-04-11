# Homie

Python implementation of Homie 3.0.1

Class based system to easily add Homie 3.0.1 support to devices.

EG.

~~~~
import time

from homie.device_dimmer import Device_Dimmer

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


class My_Dimmer(Device_Dimmer):

    def set_value(self,topic,payload):
        print('Received MQTT message to set the dimmer to {}. Must replace this method'.format(payload))
        

try:

    dimmer = My_Dimmer(name = 'Test Dimmer',mqtt_settings=mqtt_settings)
    
    while True:
        time.sleep(5)
        dimmer.update_dimmer(50)
        time.sleep(5)
        dimmer.update_dimmer(100)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")        


~~~~