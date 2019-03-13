#!/usr/bin/env python

import logging
import time
import somecomfort

from device_thermostat import Device_Thermostat



mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
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

class TCC_Device(Device_Thermostat):

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

        thermostat = TCC_Device(name = device.name,mqtt_settings=mqtt_settings)
        
        while True:
            thermostat.update (device.current_temperature,device.current_humidity,device.setpoint_cool,device.setpoint_heat,device.hold_cool,device.system_mode,device.fan_mode)
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
            time.sleep(120)
            device.refresh()

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

