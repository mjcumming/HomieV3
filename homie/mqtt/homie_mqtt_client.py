#!/usr/bin/env python

from homie.mqtt.paho_mqtt_client import PAHO_MQTT_Client

import logging
logger = logging.getLogger(__name__)


MQTT_SETTINGS = {
    'MQTT_BROKER' : None,
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : None,
    'MQTT_SHARE_CLIENT' : None,
}

mqtt_client_count = 0
    
def _mqtt_validate_settings(settings):
    global mqtt_client_count
    mqtt_client_count = mqtt_client_count + 1
    
    for setting,value in MQTT_SETTINGS.items():
        logger.debug ('MQTT Settings {} {}'.format(setting,value))
        if not setting in settings:
            settings [setting] = MQTT_SETTINGS [setting]

    assert settings ['MQTT_BROKER']
    assert settings ['MQTT_PORT']

    if settings ['MQTT_CLIENT_ID'] is None or settings ['MQTT_SHARE_CLIENT'] is False:
        settings ['MQTT_CLIENT_ID'] = 'Homie{:04d}'.format(mqtt_client_count) 
        print('client ID',settings ['MQTT_CLIENT_ID'])

    return settings

common_mqtt_client = None

def connect_mqtt_client (device,mqtt_settings):
    mqtt_settings = _mqtt_validate_settings (mqtt_settings)

    if mqtt_settings ['MQTT_SHARE_CLIENT'] is not True:
        mqtt_client = PAHO_MQTT_Client (mqtt_settings,device._on_mqtt_connection,device._on_mqtt_message)
        logger.debug ('using seperate clients')
        global mqtt_client_count
        mqtt_client_count = mqtt_client_count + 1
        
        return mqtt_client
    else:
        global common_mqtt_client
        if common_mqtt_client is None:
            common_mqtt_client = Common_MQTT_Client (mqtt_settings)

        common_mqtt_client.add_device(device)
        logger.debug ('using shared client')

        return common_mqtt_client.mqtt_client
    

class Common_MQTT_Client (object):

    def __init__(self, mqtt_settings):

        self.mqtt_client= PAHO_MQTT_Client(mqtt_settings=mqtt_settings,on_connection=self._on_mqtt_connection,on_message=self._on_mqtt_message)

        self.devices = []

    def add_device(self,device):
        self.devices.append(device)

    def remove_device(self,device): # not tested
        del self.devices [device]

    def _on_mqtt_connection(self,connected):
        for device in self.devices:
            device._on_mqtt_connection(connected)

    def _on_mqtt_message(self, topic, payload):
        for device in self.devices:
            device._on_mqtt_message(topic,payload)

'''
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        logger.debug ('MQTT Message: Topic {}, Payload {}'.format(topic,payload))

        if topic in self.mqtt_subscription_handlers:
            self.mqtt_subscription_handlers [topic] (topic, payload)        
        else:
            logger.warning ('MQTT Unknown Message: Topic {}, Payload {}'.format(topic,payload))
    
    def publish(self, topic, payload, retain=True, qos=1):
        if self.mqtt_connected:
            logger.debug('MQTT publish topic: {}, retain {}, qos {}, payload: {}'.format(topic,retain,qos,payload))
            self.mqtt_client.publish(topic, payload, retain=retain, qos=qos)
        else:
            logger.warning('MQTT not connected, unable to publish topic: {}, payload: {}'.format(topic,payload))

    def set_will(self,will,retain=True,qos=1):
        self.mqtt_client.will_set(will,retain,qos)

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


'''