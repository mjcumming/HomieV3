#!/usr/bin/env python

import logging
import sys
import time

import timer3

import paho.mqtt.client as mqtt_client
from uuid import getnode as get_mac
from homie.support.network_information import Network_Information
from homie.support.helpers import validate_id
#from homie.support.repeating_timer import Repeating_Timer

import atexit


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mqtt_logger = logging.getLogger(__name__)
mqtt_logger.setLevel('WARN')

network_info = Network_Information()

instance_count = 0 # used to track the number of device instances to allow for changing the default device id

DEVICE_STATES = [
    "init", 
    "ready", 
    "disconnected", 
    "sleeping", 
    "alert",
    "lost",
]

MQTT_SETTINGS = {
    'MQTT_BROKER' : None,
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : None,
}

HOMIE_SETTINGS = {
    'version' : '3.0.1',
    'topic' : 'homie', 
    'fw_name' : 'python',
    'fw_version' : sys.version, 
    'update_interval' : 60,
    'implementation' : sys.platform, 
}




class Device_Base(object):

    def __init__(self, device_id=None, name=None, homie_settings={}, mqtt_settings={}):
        if device_id is None:
            device_id=self.generate_device_id()

        assert validate_id(device_id), device_id
        self.device_id = device_id

        assert name
        self.name = name

        self.homie_settings = self._homie_validate_settings (homie_settings)
        
        self.mqtt_settings = self._mqtt_validate_settings (mqtt_settings)

        self._state = "init"

        self.mqtt_client= None
        self.mqtt_connected = False
        self.mqtt_subscription_handlers = {}

        #may need a way to set these
        self.retained = True
        self.qos = 1

        self.nodes = {}

        self.topic = "/".join((self.homie_settings ['topic'], self.device_id))

        self.start_time = None
    
    def generate_device_id(self):
        global instance_count
        instance_count = instance_count + 1
        return "{:02x}".format(get_mac())+"{:04d}".format(instance_count)

    def start(self): # called after the device has been built with nodes and properties
        self.start_time = time.time()

        self._mqtt_connect()

        def update_status():
            self.publish_statistics()

        self.timer = timer3.apply_interval(self.homie_settings['update_interval']* 1000, update_status, priority=0)
        #self.timer = Repeating_Timer(self.homie_settings ['update_interval'],update_status) #update the state topic 

        if self.state == 'init':
            self.state == 'ready'

    def stop_timer(self):
        self.timer.cancel()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state, retain = True, qos = 1):
        if state in DEVICE_STATES:
            self._state = state
            self.publish( "/".join((self.topic, "$state")),self._state, retain, 1)
        else:
            logging.warning ('Homie Invalid device state {}'.format(state))

    def publish_attributes(self, retain=True, qos=1):
        ip = network_info.get_local_ip (self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings ['MQTT_PORT'])
        mac = network_info.get_local_mac_for_ip(ip)

        self.publish("/".join((self.topic, "$homie")),self.homie_settings ['version'], retain, qos)
        self.publish("/".join((self.topic, "$name")),self.name, retain, qos)
        self.publish("/".join((self.topic, "$localip")),ip, retain, qos)
        self.publish("/".join((self.topic, "$mac")),mac, retain, qos)
        self.publish("/".join((self.topic, "$fw/name")),self.homie_settings ['fw_name'], retain, qos)
        self.publish("/".join((self.topic, "$fw/version")),self.homie_settings ['fw_version'], retain, qos)
        self.publish("/".join((self.topic, "$implementation")),self.homie_settings ['implementation'], retain, qos)
        self.publish("/".join((self.topic, "$stats/interval")),self.homie_settings ['update_interval'], retain, qos)

    def publish_statistics(self, retain=True, qos=1):
        self.publish("/".join((self.topic, "$stats/uptime")),time.time()-self.start_time, retain, qos)

    def add_subscription(self,topic,handler): #subscription list to the required MQTT topics, used by properties to catch set topics
        self.mqtt_subscription_handlers [topic] = handler
        self.mqtt_client.subscribe (topic,0)
        logging.info ('MQTT subscribed to {}'.format(topic))

    def subscribe_topics(self):
        self.add_subscription ("/".join((self.topic, "$broadcast/#")),self.broadcast_handler) #get the broadcast events

        for _,node in self.nodes.items():
            for topic,handler in node.get_subscriptions().items():
                self.add_subscription(topic,handler)
  
    def add_node(self,node):
        self.nodes [node.id] = node

        if self.start_time is not None: #running, publish node changes
            self.publish_nodes(self.retained, self.qos)

    def remove_node(self, node_id):
        del self.nodes [node_id]

        if self.start_time is not None: #running, publish property changes
            self.publish_nodes(retain = False)

    def get_node(self,node_id):
        if node_id in self.nodes:
            return self.nodes [node_id]
        else:
            return None

    def publish_nodes(self, retain=True, qos=1):
        nodes = ",".join(self.nodes.keys())
        self.publish("/".join((self.topic, "$nodes")), nodes, retain, qos)

        for _,node in self.nodes.items():
            node.publish_attributes(retain, qos)

    def broadcast_handler(self,topic,payload):
        logging.info ('MQTT Homie Broadcast:  Topic {}, Payload {}'.format(topic,payload))

    def publish(self, topic, payload, retain=True, qos=1):
        if self.mqtt_connected:
            logger.info('MQTT publish topic: {}, retain {}, qos {}, payload: {}'.format(topic,retain,qos,payload))
            self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)
        else:
            logger.warning('MQTT not connected, unable to publish topic: {}, payload: {}'.format(topic,payload))

    def _homie_validate_settings(self,settings):
        if settings is not None:
            for setting,value in HOMIE_SETTINGS.items():
                if not setting in settings:
                    settings [setting] = HOMIE_SETTINGS [setting]
    
            if 'MQTT_CLIENT_ID' not in settings or settings ['MQTT_CLIENT_ID'] is None:
                settings ['MQTT_CLIENT_ID'] = 'Homie_'+self.device_id
        else:
            settings = HOMIE_SETTINGS

        return settings

    def _mqtt_validate_settings(self,settings):
        for setting,value in MQTT_SETTINGS.items():
            if not setting in settings:
                settings [setting] = MQTT_SETTINGS [setting]

        assert settings ['MQTT_BROKER']
        assert settings ['MQTT_PORT']
        return settings

    def _mqtt_connect(self):
        logger.info("MQTT Connecting to {} as client {}".format(self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings['MQTT_CLIENT_ID']))

        self.mqtt_client = mqtt_client.Client(client_id=self.mqtt_settings['MQTT_CLIENT_ID'])
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.on_publish = self._on_publish
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.enable_logger(mqtt_logger)
        
        self.mqtt_client.will_set(
            "/".join((self.topic, "$state")), "lost", retain=True, qos=1
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
            logger.warning ('MQTT Unable to connect to Broker {}'.format(e))

    def _on_connect(self,client, userdata, flags, rc):
        logger.info("MQTT Connect: {}".format(rc))        

        if rc == 0:
            self.mqtt_connected = True
            self.publish_attributes()
            self.publish_nodes()
            self.subscribe_topics()
            self.state='ready'
        else:
            self.mqtt_connected = False

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        print ('topic',topic)
        print ('payload',payload)
        logging.info ('MQTT Message: Topic {}, Payload {}'.format(topic,payload))

        if topic in self.mqtt_subscription_handlers:
            self.mqtt_subscription_handlers [topic] (topic, payload)        
        else:
            logger.warning ('MQTT Unknown Message: Topic {}, Payload {}'.format(topic,payload))
    
    def _on_publish(self, *args):
        #print('MQTT Publish: Payload {}'.format(*args))
        pass

    def _on_disconnect(self):
        logger.debug("MQTT Disconnect:")        
        self.mqtt_connected = False


    def __del__(self):
        pass

        #if self.timer:
         #   self.timer.cancel()        
