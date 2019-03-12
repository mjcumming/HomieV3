
import logging

import re

def validate_id(id):
    if isinstance(id, str):
        r = re.compile('(^(?!\-)[a-z0-9\-]+(?<!\-)$)')
        return id if r.match(id) else False


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

data_types = [
    'integer',
    'float', 
    'boolean', 
    'string', 
    'enum', 
    'color',
]

class Property_Base(object):

    def __init__(self, id, name=None, settable=False, retained=True, qos=1, unit=None, data_type=None, data_format=None, value=None, set_value=None):
        assert validate_id (id), id
        self.id = id
        self.name = name
        self.retained = retained
        self.qos = qos
        self.unit = unit
        assert data_type in data_types
        self.data_type = data_type
        self.data_format = data_format
        self.settable = settable
        if settable:
            assert(set_value)
            self.set_value = set_value

        self.parent_publisher = None

        if value:
            self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.publish (self.topic,value,self.retained,self.qos)
    
    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, parent_topic):
        self._topic =  "/".join([parent_topic,self.id])

    def publish(self,topic,payload, retain, qos):
        self.parent_publisher (topic,payload,retain,qos)

    def publish_attributes(self):
        self.publish ("/".join((self.topic, "$name")), self.name, True, 1)
        self.publish ("/".join((self.topic, "$settable")), self.settable, True, 1)
        self.publish ("/".join((self.topic, "$retained")), self.retained, True, 1)
        if self.unit:
            self.publish ("/".join((self.topic, "$unit")), self.unit, True, 1)
        if self.data_type:
            self.publish ("/".join((self.topic, "$datatype")), self.data_type, True, 1)
        if self.data_format:
            self.publish ("/".join((self.topic, "$format")), self.data_format, True, 1)

    def get_subscriptions(self):
        if self.settable:
            return {"/".join((self.topic, "set")) : self.message_handler}
        else:   
            return {}

    def message_handler(self,topic,payload):
        logger.info ('MQTT Property Message:  Topic {}, Payload {}'.format(topic,payload))
        self.process_message(topic,payload)

    def process_message(self,topic,payload):
        self.set_value(topic,payload)

