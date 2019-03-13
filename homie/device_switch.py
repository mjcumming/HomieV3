#!/usr/bin/env python

from device_base import Device_Base
from node.node_base import Node_Base
from node.property.property_switch import Property_Switch



class Device_Switch(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base('switch','Switch','switch'))
        self.add_node (node)

        def set_value_function(topic,payload):
            self.set_value(topic,payload)

        self.switch = Property_Switch (set_value = set_value_function)
        node.add_property (self.switch)

        self.start()

    def update(self,on):
        if on:
            self.switch.value = 'ON'
        else:
            self.switch.value = 'OFF'

    def set_value(self,topic,payload):
        print('must override set_value',topic,payload)
        

