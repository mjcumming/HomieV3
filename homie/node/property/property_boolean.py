import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)

class Property_Boolean(Property_Base):

    def __init__(self, node, id, name, settable=True, retained=True, qos=1, unit=None, data_type='boolean', data_format=None, value=None, set_value=None):
        super().__init__(node,id,name,settable,retained,qos,unit,'boolean',data_format,value,set_value)

    def validate_value(self, value):
        return payload == 'true' or payload == 'false':

    def message_handler(self,topic,payload):
        if self.validate_value(payload):
            super().message_handler(topic,payload)
        else:
            logger.warning ('Payload boolean value invalid for property for message {}, payload is {}'.format(topic,payload))
