#!/usr/bin/env python

import logging
import time
import somecomfort

from homie.device_thermostat import Device_Honeywell_Thermostat

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
}

thermostats = {}

if __name__ == '__main__':
    try:
        
        client = somecomfort.SomeComfort('mike@4831.com','Minaki17')

        for l_name, location in client.locations_by_id.items():
            print('Location %s:' % l_name)
            for key, device in location.devices_by_id.items():
                print('  Device %s: %s' % (key, device.name))
                thermostat = Device_Honeywell_Thermostat(device_id=str(key),name = device.name,mqtt_settings=mqtt_settings,tcc_device=device)
                thermostats [key] = thermostat
           
        while True:
            time.sleep(120)
            for key,thermostat in thermostats.items():
                thermostat.update ()


    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

