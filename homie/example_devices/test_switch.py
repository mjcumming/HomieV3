#!/usr/bin/env python

import time

from homie.device_switch import Device_Switch

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


class My_Switch(Device_Switch):

    def set_value(self,topic,payload):
        print('Receive MQTT message to set the switch to {}. Must replace this method'.format(payload))
        

try:

    switch = My_Switch(name = 'Test Switch',mqtt_settings=mqtt_settings)
    
    while True:
        time.sleep(5)
        switch.update(True)
        time.sleep(5)
        switch.update(False)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")    
    switch = None    

