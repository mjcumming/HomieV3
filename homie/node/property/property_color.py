import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# ********** not completed

class Property_Color(Property_Base):

    def __init__(self, node, id, name, settable=True, retained=True, qos=1, unit=None, data_type='color', data_format=None, value=None, set_value=None):

        super().__init__(node,id,name,settable,retained,qos,unit,'color',data_format,value,set_value)

        # check valid data format provided

    def message_handler(self,topic,payload):
        if payload == 'true' or payload == 'false':  # need code to parse color values
            super().message_handler(topic,payload)
        else:
            logger.warning ('Payload boolean value invalid for property for message {}, payload is {}'.format(topic,payload))
