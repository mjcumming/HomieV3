#!/usr/bin/env python

# *** not ready for use

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_setpoint import Property_Setpoint
from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity
from homie.node.property.property_enum import Property_Enum
from homie.node.property.property_string import Property_String


FAN_MODES = ['auto', 'on', 'circulate']
SYSTEM_MODES = ['heat', 'off', 'cool']
HOLD_MODES = ['schedule', 'temporary', 'permanent'] 


class Device_Honeywell_Thermostat(Device_Base):

    tcc_device = None

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, tcc_device=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        self.tcc_device=tcc_device

        node = (Node_Base(self,'controls','Controls','controls'))
        self.add_node (node)

        heat_setpt_limits = '{}:{}'.format(tcc_device.raw_ui_data['HeatLowerSetptLimit'],tcc_device.raw_ui_data['HeatUpperSetptLimit'])
        self.heat_setpoint = Property_Setpoint (node,id='heatsetpoint',name='Heat Setpoint',data_format=heat_setpt_limits,unit=tcc_device.temperature_unit,value=tcc_device.setpoint_heat,set_value = lambda value: self.set_heat_setpoint(value) )
        node.add_property (self.heat_setpoint)

        cool_setpt_limits = '{}:{}'.format(tcc_device.raw_ui_data['CoolLowerSetptLimit'],tcc_device.raw_ui_data['CoolUpperSetptLimit'])
        self.cool_setpoint = Property_Setpoint (node,id='coolsetpoint',name='Cool Setpoint',data_format=cool_setpt_limits,unit=tcc_device.temperature_unit,value=tcc_device.setpoint_cool,set_value=lambda value: self.set_cool_setpoint(value) )
        node.add_property (self.cool_setpoint)

        self.system_mode = Property_Enum (node,id='systemmode',name='System Mode',data_format=','.join(SYSTEM_MODES),value=tcc_device.system_mode,set_value = lambda value: self.set_system_mode(value) )
        node.add_property (self.system_mode)

        self.fan_mode = Property_Enum (node,id='fanmode',name='Fan Mode',data_format=','.join(FAN_MODES),value=tcc_device.fan_mode,set_value = lambda value: self.set_fan_mode(value) )
        node.add_property (self.fan_mode)

        self.hold_mode = Property_Enum (node,id='holdmode',name='Hold Mode',data_format=','.join(HOLD_MODES),value=self.get_hold_mode(),set_value = lambda value: self.set_hold_mode(value) )
        node.add_property (self.hold_mode)

        node = (Node_Base(self,'status','Status','status'))
        self.add_node (node)

        self.temperture = Property_Temperature (node,unit=tcc_device.temperature_unit)
        node.add_property (self.temperture)

        self.humidity = Property_Humidity (node)
        node.add_property (self.humidity)

        self.system_status = Property_String (node,id='systemstatus',name='System Status',value=tcc_device.equipment_output_status)
        node.add_property (self.system_status)

        self.start()

    def get_hold_mode(self): # returns string representation of hold
        if self.tcc_device.hold_cool == True: 
            return 'permanent'
        elif self.tcc_device.hold_cool == False:
            return 'schedule'
        else:
            return 'temporary'

    def update(self):
        self.tcc_device.refresh()
        self.temperture.value = self.tcc_device.current_temperature
        self.humidity.value = self.tcc_device.current_humidity
        self.hold_mode = self.get_hold_mode()
        self.fan_mode.value = self.tcc_device.fan_mode
        self.system_mode.value = self.tcc_device.system_mode
        self.heat_setpoint.value = self.tcc_device.setpoint_heat
        self.cool_setpoint.value = self.tcc_device.setpoint_cool
        self.system_status.value = self.tcc_device.equipment_output_status

        if self.tcc_device.is_alive:
            self.state = 'ready'
        else:
            self.state = 'disconnected'

    def set_heat_setpoint(self,value):
        self.tcc_device.setpoint_heat=value
        self.heat_setpoint.value = value
        
    def set_cool_setpoint(self,value):
        self.tcc_device.setpoint_cool=value
        self.cool_setpoint.value = value
        
    def set_system_mode(self,value):
        self.tcc_device.system_mode=value
        self.system_mode.value=value
        
    def set_fan_mode(self,value):
        self.tcc_device.fan_mode = value
        self.fan_mode = value
        
    def set_hold_mode(self,value):
        if value == 'permanent':
            self.tcc_device.hold_heat = True
            self.tcc_device.hold_cool = True
        elif value == 'schedule':
            self.tcc_device.hold_heat = False
            self.tcc_device.hold_cool = False
        else:
            print('unknown hold mode: ',value)
        
