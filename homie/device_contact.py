#!/usr/bin/env python

from device_base import Device_Base
from node.node_base import Node_Base
from node.property.switch import Switch



class Device_Contact(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base('contact','Contact','contact'))
        self.add_node (node)


        self.contact = Contact()
        node.add_property (self.contact)

        self.start()

    def update(self,open):
        if on:
            self.switch.value = 'OPEN'
        else:
            self.switch.value = 'CLOSED'


