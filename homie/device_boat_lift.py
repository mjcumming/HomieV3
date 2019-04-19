#!/usr/bin/env python

# *** not ready for use

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_string import Property_String
from homie.node.property.property_integer import Property_Integer

LIFT_MODES = ['LIFT','LIFT_MAX','LOWER','STOP']


class Device_Boat_Lift(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(device,'controls','Controls','controls'))
        self.add_node (node)

        self.lift_control = Property_Setpoint (node,id='control',name='Lift Control',data.format=','.join(LIFT_MODES),set_value = lambda value: self.set_lift_mode(value) )
        node.add_property (self.lift_control)

        node = (Node_Base(device,'status','Lift Status','status'))
        self.add_node (node)

        self.pitch = Property_String (node,id='pitch',name='Pitch')
        node.add_property (node,self.pitch)

        self.roll = Property_String (node,id='roll',name='Pitch')
        node.add_property (node,self.roll)

        self.current_mode = Property_String (node,'mode','Mode')
        node.add_property (node,self.mode)

        self.position = Property_String (node,id='position',name='Position',)
        node.add_property (node,self.position)

        self.start()

    def update(self,position,pitch,roll,mode):
        self.temperture.value = temperature
        self.humidity.value = humidity
        self.hold_mode = hold_mode
        self.fan_mode = fan_mode
        self.system_mode = system_mode
        self.heat_setpoint = heat_setpoint
        self.cool_setpoint = cool_setpoint

    def set_lift_mode(self,value):
        print('set_value - need to overide',value)
        
    