#!/usr/bin/env python

# *** not ready for use

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_setpoint import Property_Setpoint
from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity
from homie.node.property.property_enum import Property_Enum
from homie.node.property.property_string import Property_String


FAN_MODES = ['auto', 'on', 'circulate', 'follow schedule']
SYSTEM_MODES = ['emheat', 'heat', 'off', 'cool', 'auto', 'auto']
HOLD_MODES = ['schedule', 'temporary', 'permanent']
EQUIPMENT_OUTPUT_STATUS = ['off/fan', 'heat', 'cool']


class Device_Thermostat(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, unit='F'):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(device,'controls','Controls','controls'))
        self.add_node (node)

        self.heat_setpoint = Property_Setpoint (node,id='heatsetpoint',name='Heat Setpoint',set_value = lambda value: self.set_heat_setpoint(value) )
        node.add_property (self.heat_setpoint)

        self.cool_setpoint = Property_Setpoint (node,id='coolsetpoint',name='Cool Setpoint',set_value = lambda value: self.set_cool_setpoint(value) )
        node.add_property (self.cool_setpoint)

        self.system_mode = Property_Enum (node,id='systemmode',name='System Mode',data_format=','.join(SYSTEM_MODES),set_value = lambda value: self.set_system_mode(value) )
        node.add_property (self.system_mode)

        self.fan_mode = Property_Enum (node,id='fanmode',name='Fan Mode',data_format=','.join(FAN_MODES),set_value = lambda value: self.set_fan_mode(value) )
        node.add_property (self.fan_mode)

        self.hold_mode = Property_Enum (node,id='holdmode',name='Hold Mode',data_format=','.join(HOLD_MODES),set_value = lambda value: self.set_hold_mode(value) )
        node.add_property (self.hold_mode)

        node = (Node_Base(device,'status','Status','status'))
        self.add_node (node)

        self.temperture = Property_Temperature (node,unit=unit)
        node.add_property (node,self.temperture)

        self.humidity = Property_Humidity (node)
        node.add_property (node,self.humidity)

        self.system_status = Property_String (node,id='systemstatus',name='System Status',)
        node.add_property (node,self.system_status)

        self.start()

    def update(self,temperature,humidity,cool_setpoint,heat_setpoint,hold_mode,system_mode,fan_mode):
        self.temperture.value = temperature
        self.humidity.value = humidity
        self.hold_mode = hold_mode
        self.fan_mode = fan_mode
        self.system_mode = system_mode
        self.heat_setpoint = heat_setpoint
        self.cool_setpoint = cool_setpoint

    def set_heat_setpoint(self,value):
        print('set_value - need to overide',value)
        
    def set_cool_setpoint(self,value):
        print('set_value - need to overide',value)
        
    def set_system_mode(self,value):
        print('set_value - need to overide',value)
        
    def set_fan_mode(self,value):
        print('set_value - need to overide',value)
        
    def set_hold_mode(self,value):
        print('set_value - need to overide',value)
        
