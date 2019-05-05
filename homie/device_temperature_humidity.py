#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity

import logging

logger = logging.getLogger(__name__)

class Device_Temperature_Humidity(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, temp_units='F'):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(self,'status','Status','status'))
        self.add_node (node)

        self.temperature = Property_Temperature (node,unit=temp_units)
        node.add_property (self.temperature)

        self.humidity = Property_Humidity (self)
        node.add_property (self.humidity)

        self.start()

    def update(self,temperature,humidity):
        logging.info ('Updated Temperature {}, Humidity {}'.format(temperature,humidity))
        self.temperature.value = temperature
        self.humidity.value = humidity

