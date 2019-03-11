#!/usr/bin/env python

import sys
import time
from network_information import Network_Information


from device_base import Device_Base
from node.node_base import Node_Base
from node.property.switch import Switch
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




class Switch_Device(Device_Base):

    def __init__(self, device_id='switch', name='Switch', homie_topic='homie', fw_name='python',fw_version=sys.version, update_interval=60, implementation=sys.platform, mqtt_settings=mqtt_settings):

        Device_Base.__init__ (self, device_id, name, homie_topic, fw_name, fw_version, update_interval, implementation, mqtt_settings)

        node = (Node_Base('switch','Switch','switch'))
        self.add_node (node)

        switch_property = Switch ()
        node.add_property (switch_property)

if __name__ == '__main__':
    try:

        hd = Switch_Device(name = 'Test Switch')
        hd.start()
        time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

