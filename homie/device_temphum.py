#!/usr/bin/env python

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base

from homie.node.property.property_temperature import Property_Temperature
from homie.node.property.property_humidity import Property_Humidity

class Device_TempHum(Device_Base):

    def __init__(self, device_id=None, name=None, homie_settings=None, mqtt_settings=None, temp_units='F'):

        super().__init__ (device_id, name, homie_settings, mqtt_settings)

        node = (Node_Base(self,'status','Status','status'))
        self.add_node (node)

        self.temperture = Property_Temperature (node,unit=temp_units)
        node.add_property (self.temperture)

        self.humidity = Property_Humidity (self)
        node.add_property (self.humidity)

        self.start()

    def update(self,temperature,humidity):
        self.temperture.value = temperature
        self.humidity.value = humidity

