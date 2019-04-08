#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_contact import Property_Contact



class Device_Contact(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base('contact','Contact','contact'))
        self.add_node (node)

        self.contact = Property_Contact()
        node.add_property (self.contact)

        self.start()

    def update(self,open):
        if open:
            self.contact.value = 'OPEN'
        else:
            self.contact.value = 'CLOSED'


