
import logging

import re

def validate_id(id):
    if isinstance(id, str):
        r = re.compile('(^(?!\-)[a-z0-9\-]+(?<!\-)$)')
        return id if r.match(id) else False


logger = logging.getLogger(__name__)


data_types = [
    'integer',
    'float', 
    'boolean', 
    'string', 
    'enum', 
    'color',
]

class Property_Base(object):

    def __init__(self, node, id, name=None, settable=False, retained=True, qos=1, unit=None, data_type=None, data_format=None, value=None, set_value=None):
        if validate_id (id) is False:
            logger.error('Property ID not valid {}'.format(id))
            assert validate_id(id),'Property ID is not valid {}'.format(id)

        self.id = id
        self.name = name
        self.retained = retained
        self.qos = qos
        self.unit = unit
        self.node = node

        self.topic = node.topic
        
        assert data_type in data_types
        self.data_type = data_type
        self.data_format = data_format
        
        self.settable = settable
        if settable: # must provide a function to call to set the value
            assert(set_value)
            self.set_value = set_value

        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value, retain=True, qos=1):
        if self.validate_value(value):
            self._value = value
            self.publish (self.topic,value,retain,qos)
            logger.debug ('Value set to:   {}'.format(value))
        else:
            logger.warn ('Invalid Value: Device {} Node {} Property {} Value {}'.format(self.node.device.name,self.node.name,self.name,value))

    def validate_value(self,value):
        return True # override as needed

    def get_value_from_payload(self,payload):
        return payload
    
    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, parent_topic):
        self._topic =  "/".join([parent_topic,self.id])

    def publish(self, topic, payload, retain, qos):
        self.node.property_publisher (topic,payload,retain,qos)

    def publish_attributes(self, retain=True, qos=1):
        self.publish ("/".join((self.topic, "$name")), self.name, retain, qos)
        self.publish ("/".join((self.topic, "$settable")), self.settable, retain, qos)
        self.publish ("/".join((self.topic, "$retained")), self.retained, retain, qos)
        if self.unit:
            self.publish ("/".join((self.topic, "$unit")), self.unit, retain, qos)
        if self.data_type:
            self.publish ("/".join((self.topic, "$datatype")), self.data_type, retain, qos)
        if self.data_format:
            self.publish ("/".join((self.topic, "$format")), self.data_format, retain, qos)

        if self.value is not None: # publish value if known, by setting it
            self.value = self.value

    def get_subscriptions(self): # subscribe to the set topic
        if self.settable:
            return {"/".join((self.topic, "set")) : self.set_message_handler}
        else:   
            return {}

    def set_message_handler(self,topic,payload):
        logger.debug ('MQTT Property Message:  Topic {}, Payload {}'.format(topic,payload))
        self.process_set_message(topic,payload)

    def process_set_message(self,topic,payload): #override as needed
        value = self.get_value_from_payload(payload)

        if value is not None:
            if self.validate_value(value):
                self.value = value
                self.set_value(value) # call function to actually change the value
            else:
                logger.warning ('Payload value not valid for property for topic {}, payload is {}'.format(topic,payload))
        else:
            logger.warning ('Unable to convert payload for property topic {}, payload is {}'.format(topic,payload))


