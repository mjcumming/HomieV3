import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Property_Enum(Property_Base):

    def __init__(self, id, name, settable=True, retained=True, qos=1, unit=None, data_type='enum', data_format=None, value=None, set_value=None):
        assert(data_format)
        super().__init__(id,name,settable,retained,qos,unit,data_type,data_format,value,set_value)

        self.enum_list = data_format.split(',')

    def message_handler(self,topic,payload):
        if payload in self.enum_list:
            super().message_handler(topic,payload)
        else:
            logger.warning ('Invalid payload for enum property message {}, payload is {}'.format(topic,payload))

 