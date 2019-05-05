#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_temperature import Property_Temperature

import logging

logger = logging.getLogger(__name__)

class Device_Temperature(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, temp_units='F'):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(self,'status','Status','status'))
        self.add_node (node)

        self.temperature = Property_Temperature (node,unit=temp_units)
        node.add_property (self.temperature)

        self.start()

    def update(self,temperature):
        logging.info ('Updated Temperature {}'.format(temperature))
        self.temperature.value = temperature

