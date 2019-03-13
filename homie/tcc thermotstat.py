#!/usr/bin/env python

import logging
import time
import somecomfort

from thermostat_device import Thermostat_Device


from uuid import getnode as get_mac


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)



def generate_device_id():
    return "{:02x}".format(get_mac())


mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : 'Homie_'+generate_device_id(),
}

client = somecomfort.SomeComfort('mike@4831.com','Minaki17')

for l_name, location in client.locations_by_id.items():
    print('Location %s:' % l_name)
    for key, device in location.devices_by_id.items():
        print('  Device %s: %s' % (key, device.name))
        
        
device = client.default_device



FAN_MODES = ['auto', 'on', 'circulate', 'follow schedule']
SYSTEM_MODES = ['emheat', 'heat', 'off', 'cool', 'auto', 'auto']
HOLD_MODES = ['schedule', 'temporary', 'permanent']
EQUIPMENT_OUTPUT_STATUS = ['off/fan', 'heat', 'cool']

class TCC_Device(Thermostat_Device):

    def __init__(self, device_id='thermostat', name='Thermostat', update_interval=60,  mqtt_settings=mqtt_settings):

        super().__init__ (device_id=device_id, name=name, update_interval=update_interval, mqtt_settings=mqtt_settings)

    def set_heat_setpoint(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        
    def set_cool_setpoint(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        
    def set_system_mode(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        
    def set_fan_mode(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        
    def set_hold_mode(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        

if __name__ == '__main__':
    try:

        thermostat = TCC_Device(name = device.name)
        
        while True:
            time.sleep(5)
            thermostat.update (device.current_temperature,device.current_humidity)
            print(device.name)
            print(device.is_alive)

            print(device.temperature_unit)
            print(device.current_temperature)
            print(device.current_humidity)

            print(device.hold_heat)
            print(device.hold_cool)

            print(device.fan_mode)
            print(device.fan_running)

            print(device.system_mode)

            print(device.setpoint_cool)

            print(device.setpoint_heat)

            print(device.outdoor_temperature)

            print(device.outdoor_humidity)

            print(device.equipment_output_status)
            print(device.raw_ui_data)
            print(device.raw_fan_data)
            print(device.raw_dr_data)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

