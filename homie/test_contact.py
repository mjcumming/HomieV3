#!/usr/bin/env python

import time

from device_contact import Device_Contact

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}


try:

    contact = Device_Contact(name = 'Test Contact',mqtt_settings=mqtt_settings)
    
    while True:
        time.sleep(5)
        contact.update(True)
        time.sleep(5)
        contact.update(False)

except (KeyboardInterrupt, SystemExit):
    print("Quitting.")        
    quit()
