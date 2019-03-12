#!/usr/bin/env python

import sys
import time
from network_information import Network_Information


from device_base import Device_Base
from node.node_base import Node_Base
from node.property.dimmer import Dimmer
from uuid import getnode as get_mac


def generate_device_id():
    return "{:02x}".format(get_mac())

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : 'Homie_'+generate_device_id(),
}


class Dimmer_Device(Device_Base):

    def __init__(self, device_id='dimmer', name='Dimmer', homie_topic='homie', fw_name='python',fw_version=sys.version, update_interval=60, implementation=sys.platform, mqtt_settings=mqtt_settings):

        super().__init__ (device_id, name, homie_topic, fw_name, fw_version, update_interval, implementation, mqtt_settings)

        node = (Node_Base('dimmer','Dimmer','dimmer'))
        self.add_node (node)

        def callback_function(topic,message):
            self.callback(topic,message)

        self.dimmer = Dimmer (callback = callback_function)
        node.add_property (self.dimmer)

        self.start()

    def update(self,percent):
        self.dimmer.value = percent

    def callback(self,topic,message):
        print('call back',topic,message)
        

if __name__ == '__main__':
    try:

        dimmer = Dimmer_Device(name = 'Test Dimmer')
        
        while True:
            time.sleep(5)
            dimmer.update(50)
            time.sleep(5)
            dimmer.update(100)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

