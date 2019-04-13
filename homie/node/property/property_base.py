
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
        assert validate_id (id), id
        assert node

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

        if value:
            self._value = value
        else:
            self._value = False 

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.validate_value(value):
            self._value = value
            self.publish (self.topic,value,self.retained,self.qos)
            logger.debug ('Value set to:   {}'.format(value))
        else:
            logger.warn ('Invalid Value:   {}'.format(value))

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

    def publish(self,topic,payload, retain, qos):
        self.node.publish (topic,payload,retain,qos)

    def publish_attributes(self):
        self.publish ("/".join((self.topic, "$name")), self.name, True, self.qos)
        self.publish ("/".join((self.topic, "$settable")), self.settable, True, self.qos)
        self.publish ("/".join((self.topic, "$retained")), self.retained, True, self.qos)
        if self.unit:
            self.publish ("/".join((self.topic, "$unit")), self.unit, True, self.qos)
        if self.data_type:
            self.publish ("/".join((self.topic, "$datatype")), self.data_type, True, self.qos)
        if self.data_format:
            self.publish ("/".join((self.topic, "$format")), self.data_format, True, self.qos)

        if self.value: # publish value if known, by setting it
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
                logger.warning ('Payload float value out of range for property for message {}, payload is {}, low value {}. high value {}'.format(topic,payload,self.low_value,self.high_value))
        else:
            logger.warning ('Unable to convert payload for property message {}, payload is {}'.format(topic,payload))


