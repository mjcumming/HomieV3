#!/usr/bin/env python

from device_base import Device_Base
from node.node_base import Node_Base

from node.property.property_setpoint import Property_Setpoint
from node.property.property_temperature import Property_Temperature
from node.property.property_humidity import Property_Humidity
from node.property.property_enum import Property_Enum
from node.property.property_string import Property_String


FAN_MODES = ['auto', 'on', 'circulate', 'follow schedule']
SYSTEM_MODES = ['emheat', 'heat', 'off', 'cool', 'auto', 'auto']
HOLD_MODES = ['schedule', 'temporary', 'permanent']
EQUIPMENT_OUTPUT_STATUS = ['off/fan', 'heat', 'cool']


class Thermostat_Device(Device_Base):

    def __init__(self, device_id='thermostat', name='Thermostat', homie_topic='homie', fw_name='python',fw_version=sys.version, update_interval=60, implementation=sys.platform, mqtt_settings=mqtt_settings):

        super().__init__ (device_id, name, homie_topic, fw_name, fw_version, update_interval, implementation, mqtt_settings)

        node = (Node_Base('controls','Controls','controls'))
        self.add_node (node)

        self.heat_setpoint = Setpoint (id='heatsetpoint',name='Heat Setpoint',set_value = lambda topic,payload: self.set_heat_setpoint(topic,payload) )
        node.add_property (self.heat_setpoint)

        self.cool_setpoint = Setpoint (id='coolsetpoint',name='Cool Setpoint',set_value = lambda topic,payload: self.set_cool_setpoint(topic,payload) )
        node.add_property (self.cool_setpoint)

        self.system_mode = Property_Enum (id='systemmode',name='System Mode',data_format=','.join(SYSTEM_MODES),set_value = lambda topic,payload: self.set_system_mode(topic,payload) )
        node.add_property (self.system_mode)

        self.fan_mode = Property_Enum (id='fanmode',name='Fan Mode',data_format=','.join(FAN_MODES),set_value = lambda topic,payload: self.set_fan_mode(topic,payload) )
        node.add_property (self.fan_mode)

        self.hold_mode = Property_Enum (id='holdmode',name='Hold Mode',data_format=','.join(HOLD_MODES),set_value = lambda topic,payload: self.set_hold_mode(topic,payload) )
        node.add_property (self.hold_mode)

        node = (Node_Base('status','Status','status'))
        self.add_node (node)

        self.temperture = Temperature ()
        node.add_property (self.temperture)

        self.humidity = Humidity ()
        node.add_property (self.humidity)

        self.system_status = Property_String (id='systemstatus',name='System Status',)
        node.add_property (self.system_status)

        self.start()

    def update(self,temperature,humidity):#,cool_setpoint,heat_setpoint):
        self.temperture.value = temperature
        self.humidity.value = humidity

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

        thermostat = Thermostat_Device(name = 'Test Thermostat')
        
        while True:
            time.sleep(5)
            thermostat.update(60,80)
            time.sleep(5)
            thermostat.update(90,20)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

