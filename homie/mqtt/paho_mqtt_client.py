#!/usr/bin/env python

import paho.mqtt.client as mqtt_client

import traceback

from uuid import getnode as get_mac
from homie.support.network_information import Network_Information

import logging
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

mqtt_logger = logging.getLogger('MQTT')
mqtt_logger.setLevel('INFO')

MQTT_SETTINGS = {
    'MQTT_BROKER' : None,
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : None,
}

COONNECTION_RESULT_CODES = {
    0: 'Connection successful',
    1: 'Connection refused - incorrect protocol version',
    2: 'Connection refused - invalid client identifier',
    3: 'Connection refused - server unavailable',
    4: 'Connection refused - bad username or password',
    5: 'Connection refused - not authorised',
}

network_info = Network_Information()

# wrapper arond the paho mqtt

class PAHO_MQTT_Client (object):

    def __init__(self, mqtt_settings={},on_connection=None,on_message=None):
        logger.info('Using PAHO MQTT Client. Settings {}'.format(mqtt_settings))
        self.mqtt_settings = mqtt_settings

        self.mqtt_client= None
        self.mqtt_connected = False

        self.on_connection = on_connection # callback for connection status, True connected, False not connected
        self.on_message = on_message # callback for MQTT messages, used for logging, message callbacks should use subscriptions below

        self.mqtt_subscription_handlers = {}

    def connect(self):
        logger.debug("MQTT Connecting to {} as client {}".format(self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings['MQTT_CLIENT_ID']))

        self.mqtt_client = mqtt_client.Client()#client_id=self.mqtt_settings['MQTT_CLIENT_ID'])
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.on_publish = self._on_publish
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.enable_logger(mqtt_logger)
        self.mqtt_client.enable_logger()

        if self.mqtt_settings ['MQTT_USERNAME']:
            self.mqtt_client.username_pw_set(
                    self.mqtt_settings ['MQTT_USERNAME'],
                    password=self.mqtt_settings ['MQTT_PASSWORD']
            )

        try:
            self.mqtt_client.connect(
                self.mqtt_settings ['MQTT_BROKER'],
                port=self.mqtt_settings ['MQTT_PORT'],
                keepalive=self.mqtt_settings ['MQTT_KEEPALIVE'],
            )

            self.mqtt_client.loop_start()

        except Exception as e:
            logger.warning ('MQTT Unable to connect to Broker {}'.format(e))

    def publish(self, topic, payload, retain=True, qos=0):
        if self.mqtt_connected:
            logger.debug('MQTT publish topic: {}, retain {}, qos {}, payload: {}'.format(topic,retain,qos,payload))
            self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)
        else:
            logger.warning('MQTT not connected, unable to publish topic: {}, payload: {}'.format(topic,payload))

    def set_will(self,will,topic,retain=True,qos=1):
        logger.info ('MQTT set will {}, topic {}'.format(will,topic))
        self.mqtt_client.will_set(will,topic,retain,qos)

    def add_subscription(self,topic,handler,qos=0): #subscription list to the required MQTT topics, used by properties to catch set topics
        self.mqtt_subscription_handlers [topic] = handler
        self.mqtt_client.subscribe (topic,qos)
        logger.debug ('MQTT subscribed to {}'.format(topic))    
        
    def remove_subscription(self,topic):
        self.mqtt_client.unsubscribe (topic)
        del self.mqtt_subscription_handlers [topic] 
        logger.debug ('MQTT unsubscribed to {}'.format(topic))    

    def get_mac_ip_address(self):
        ip = network_info.get_local_ip (self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings ['MQTT_PORT'])
        mac = network_info.get_local_mac_for_ip(ip)

        return mac,ip

    def _on_connect(self,client, userdata, flags, rc):
        logger.debug("MQTT On Connect: {}".format(rc))       

        connected = None
        if rc == 0:
            connected = True
        else:
            connected = False

        if self.mqtt_connected != connected:
            self.mqtt_connected = connected
            logger.debug('MQTT Connection Status changed to {}'.format(connected))

            if self.mqtt_connected:
                try:
                    self.on_connection(self.mqtt_connected)

                except Exception as ex:
                    logger.error('Device On Connect Error {}'.format(ex))
                    traceback.print_exc()

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        logger.debug ('MQTT On Message: Topic {}, Payload {}'.format(topic,payload))

        self.on_message (topic,payload)

        if topic in self.mqtt_subscription_handlers:
            self.mqtt_subscription_handlers [topic] (topic, payload)        
        else:
            logger.warning ('MQTT Unknown Message: Topic {}, Payload {}'.format(topic,payload))        

    def _on_publish(self, *args):
        #logger.debug('MQTT Publish: Payload {}'.format(*args))
        pass

    def _on_disconnect(self,client,userdata,rc):
        if self.mqtt_connected:
            self.mqtt_connected = False
            self.on_connection(self.mqtt_connected)

        if rc > 0: #unexpected disconnect
            rc_text = 'Unknown result code {}'.format(rc)
            if rc in COONNECTION_RESULT_CODES:
                rc_text = COONNECTION_RESULT_CODES [rc]

            logger.warn ('MQTT Unexpected disconnection  {} {} {}'.format(client,userdata,rc_text))
        
