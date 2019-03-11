#!/usr/bin/env python


import logging
import sys
import time
import binascii
import paho.mqtt.client as mqtt_client
from uuid import getnode as get_mac
from network_information import Network_Information
from helpers import validate_id

from node.node_base import Node_Base
from node.property.property_base import Property_Base
from node.property.switch import Switch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.debug("Initializing MQTT")

mqtt_logger = logging.getLogger(__name__)
mqtt_logger.setLevel('INFO')

network_info = Network_Information()

def generate_device_id():
    return "{:02x}".format(get_mac())

HOMIE_VERSION = '3.0.1'
       
device_states = [
    "init", 
    "ready", 
    "disconnected", 
    "sleeping", 
    "alert",
]

mqtt_settings = {
    'MQTT_BROKER' : 'QueenMQTT',
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : 'Homie_'+generate_device_id(),
}




class Device_Base(object):

    def __init__(self, device_id=generate_device_id(), name=None, homie_topic='homie', fw_name='python',fw_version=sys.version, update_interval=60, implementation=sys.platform, mqtt_settings=mqtt_settings):
        assert validate_id(device_id), device_id
        self.device_id = device_id
        assert name
        self.name = name
        self.fw_version = fw_version
        self.fw_name = fw_name
        self.implementation = implementation
        self.update_interval = update_interval

        self.mqtt_settings = self._mqtt_validate_settings (mqtt_settings)

        self._state = "init"

        self.mqtt_client= None

        self.nodes = {}
        self.subscription_handlers = {}

        self.start_time = time.time()
        self.next_update = time.time()

        self.device_topic = "/".join((homie_topic, self.device_id))

        self.add_subscription ("/".join((self.device_topic, "$broadcast/#")),self.broadcast_handler)

    def start(self):
        self._mqtt_connect()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state in device_states:
            self._state = state
            self.publish( "/".join((self.device_topic, "$state")),self._state)
        else:
            logging.warning ('invalid device state {}'.format(state))

    def publish_attributes(self):
        ip = network_info.get_local_ip (self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings ['MQTT_PORT'])
        mac = network_info.get_local_mac_for_ip(ip)

        self.publish("/".join((self.device_topic, "$homie")),HOMIE_VERSION)
        self.publish("/".join((self.device_topic, "$name")),self.name)
        self.publish("/".join((self.device_topic, "$localip")),ip)
        self.publish("/".join((self.device_topic, "$mac")),mac)
        self.publish("/".join((self.device_topic, "$fw/name")),self.fw_name)
        self.publish("/".join((self.device_topic, "$fw/version")),self.fw_version)
        self.publish("/".join((self.device_topic, "$implmentation")),self.implementation)
        self.publish("/".join((self.device_topic, "$stats/interval")),self.update_interval)

    def publish_statistics(self):
        self.publish("/".join((self.device_topic, "$stats/uptime")),time.time()-self.start_time)
        #self.publish("/".join((self.device_topic, "$")),self.)

    def add_subscription(self,topic,handler):
        self.subscription_handlers [topic] = handler

    def subscribe_topics(self):
        for topic in self.subscription_handlers:
            self.mqtt_client.subscribe (topic,0)
            logging.info ('MQTT subscribed to {}'.format(topic))
  
    def add_node(self,node):
        self.nodes [node.id] = node
        node.topic = self.device_topic
        node.parent_publisher = self.publish

        for topic,handler in node.get_subscriptions().items():
            self.subscribe_topics(topic,handler)

    def publish_nodes(self):
        nodes = "/".join(self.nodes.keys())
        self.publish("/".join((self.device_topic, "$nodes")),nodes)
        for id,node in self.nodes.items():
            node.publish_attributes()

    def broadcast_handler(self,topic,payload):
        logging.info ('Homie Broadcast:  Topic {}, Payload {}'.format(topic,payload))


    def _mqtt_validate_settings(self,settings):
        for setting,value in mqtt_settings.items():
            if not setting in settings:
                settings [setting] = mqtt_settings [setting]
            #print (setting, settings [setting])
 
        return settings

    def _mqtt_connect(self):
        self.mqtt_client = mqtt_client.Client(client_id=self.mqtt_settings['MQTT_CLIENT_ID'])
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.on_publish = self._on_publish
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.enable_logger(mqtt_logger)
        
        self.mqtt_client.will_set(
            "/".join((self.device_topic, "$state")), "lost", retain=True, qos=1
        )

        if self.mqtt_settings ['MQTT_USERNAME']:
            self.mqtt_client.username_pw_set(
                    self.mqtt_settings ['MQTT_USERNAME'],
                    password=self.mqtt_settings ['MQTT_PASSWORD']
            )

        try:
            self.mqtt_client.connect_async(
                self.mqtt_settings ['MQTT_BROKER'],
                port=self.mqtt_settings ['MQTT_PORT'],
                keepalive=self.mqtt_settings ['MQTT_KEEPALIVE'],
            )

            self.mqtt_client.loop_start()
        except Exception as e:
            logging.warning ('Unable to connect to MQTT Broker {}'.format(e))

    def _on_connect(self,client, userdata, flags, rc):
        logger.debug("_connect: {}".format(rc))        

        if rc == 0:
            self.mqtt_connected = True
            self.publish_attributes()
            self.publish_nodes()
            self.state='ready'
        else:
            self.mqtt_connected = False

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        logging.info ('MQTT Message: Topic {}, Payload {}'.format(topic,payload))

        if topic in self.subscription_handlers:
            self.subscription_handlers [topic] (topic, payload)        
  
    def _on_publish(self, *args):
        #print('MQTT Publish: Payload {}'.format(*args))
        pass

    def _on_disconnect(self):
        logger.debug("_disconnect:")        
        self.mqtt_connected = False

    def publish(self, topic, payload, retain=True, qos=1):
        if self.mqtt_connected:
            logger.info('publish topic: {}, payload: {}'.format(topic,payload))
            self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)
        else:
            logger.warning('not connected, unable to publish topic: {}, payload: {}'.format(topic,payload))


if __name__ == '__main__':
    try:

        hd = Device_Base(name = 'Test')

        test_node = Node_Base('test-id','test_name','test_type')
        hd.add_node(test_node)

        test_property = Property_Base('test-property-1')
        test_node.add_property (test_property)
        test_property = Property_Base('test-property-2')
        test_node.add_property (test_property)
        test_property = Switch('test-switch-1')
        test_node.add_property (test_property)


        hd.start()
        time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")        

