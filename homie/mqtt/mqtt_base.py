#!/usr/bin/env python


'''

Base MQTT Client for a Homie device

To allow for easy replacement of the MQTT client

'''
from homie.support.network_information import Network_Information
network_info = Network_Information()

import logging
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

MQTT_SETTINGS = {
    'MQTT_BROKER' : None,
    'MQTT_PORT' : 1883,
    'MQTT_USERNAME' : None,
    'MQTT_PASSWORD' : None,
    'MQTT_KEEPALIVE' : 60,
    'MQTT_CLIENT_ID' : None,
    'MQTT_SHARE_CLIENT' : False,
}

class MQTT_Base (object):

    def __init__(self, mqtt_settings, homie_device):
        logger.info('MQTT client Settings {}'.format(mqtt_settings))
        self.mqtt_settings = self._validate_mqtt_settings (mqtt_settings)
        self.using_shared_mqtt_client = mqtt_settings ['MQTT_SHARE_CLIENT']

        self._mqtt_connected = False

        self.device = homie_device

    def _validate_mqtt_settings(self,settings):
        for setting,_ in MQTT_SETTINGS.items():
            if not setting in settings:
                settings [setting] = MQTT_SETTINGS [setting]
        assert settings ['MQTT_BROKER']
        assert settings ['MQTT_PORT']

        return settings

    @property
    def mqtt_connected(self):
        return self._mqtt_connected

    @mqtt_connected.setter
    def mqtt_connected(self,connected):
        if connected != self._mqtt_connected:
            logger.debug("MQTT Connected {} ".format(connected))
            self._mqtt_connected = connected

            self.device.mqtt_on_connection(self.mqtt_connected)

    def connect(self): #called by the device when its ready for the mqtt client to start, subclass to provide
        logger.debug("MQTT Connecting to {} as client {}".format(self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings['MQTT_CLIENT_ID']))

    def publish(self, topic, payload, retain=True, qos=0): #subclass to provide
        logger.debug('MQTT publish topic: {}, payload: {}, retain {}, qos {}'.format(topic,payload,retain,qos))

    def set_will(self,will,topic,retain=True,qos=1): #subclass to provide
        logger.info ('MQTT set will {}, topic {}'.format(will,topic))

    def get_mac_ip_address(self):
        ip = network_info.get_local_ip (self.mqtt_settings ['MQTT_BROKER'],self.mqtt_settings ['MQTT_PORT'])
        mac = network_info.get_local_mac_for_ip(ip)

        return mac,ip

    def _on_message(self,topic,payload):
        logger.debug ('MQTT On Message: Topic {}, Payload {}'.format(topic,payload))
        self.device.mqtt_on_message (topic,payload)
      

        
