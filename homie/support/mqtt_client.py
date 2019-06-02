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




class MQTT_Client (object):

    def __init__(self, homie_settings={}, mqtt_settings={}, device=None, mqtt_client = None):

        self.homie_settings = self._homie_validate_settings (homie_settings)
        
        self.mqtt_settings = self._mqtt_validate_settings (mqtt_settings)

        self.mqtt_client= None
        self.mqtt_connected = False
        self.mqtt_subscription_handlers = {}

        self._mqtt_connect()

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
        logger.debug("MQTT Connecting to {} as client {}".format(self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings['MQTT_CLIENT_ID']))

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

            self.mqtt_connected = True # assume we are good to go

            self.mqtt_client.loop_start()
        except Exception as e:
            logger.warning ('MQTT Unable to connect to Broker {}'.format(e))

    def _on_connect(self,client, userdata, flags, rc):
        logger.debug("MQTT Connect: {}".format(rc))        

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

        logger.debug ('MQTT Message: Topic {}, Payload {}'.format(topic,payload))

        if topic in self.mqtt_subscription_handlers:
            self.mqtt_subscription_handlers [topic] (topic, payload)        
        else:
            logger.warning ('MQTT Unknown Message: Topic {}, Payload {}'.format(topic,payload))
    
    def _on_publish(self, *args):
        #print('MQTT Publish: Payload {}'.format(*args))
        pass

    def _on_disconnect(self,*args):
        logger.debug("MQTT Disconnect:")        
        self.mqtt_connected = False


