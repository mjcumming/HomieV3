#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_dimmer import Property_Dimmer


class Device_Dimmer(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base('dimmer','Dimmer','dimmer'))
        self.add_node (node)

        self.dimmer = Property_Dimmer (set_value = lambda topic,payload: self.set_value(topic,payload) )
        node.add_property (self.dimmer)

        self.start()

    def update(self,percent):
        self.dimmer.value = percent

    def set_value(self,topic,payload):
        print('set_value - need to overide',topic,payload)
        
