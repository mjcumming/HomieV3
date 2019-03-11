import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Property_Integer(Property_Base):

    def __init__(self, id, name, settable=True, retained=True, qos=1, unit=None, data_type='integer', data_format=None, value=None, callback=None):
        Property_Base.__init__(self,id,name,settable,retained,qos,unit,data_type,data_format,value,callback)

        if data_format:
            range = data_format.split(':')
            self.low_value = int(range[0])
            self.high_value = int(range[1])
        else:
            self.low_value = None
            self.high_value = None

    def message_handler(self,topic,payload):
        try:
            value = int(payload)
            if self.low_value and value > self.low_value and self.high_value and value < self.high_value:
                Property_Base.message_handler(self,topic,payload)
            else:
                logging.warning ('Payload integer value out of range for property message {}, payload is {}'.format(topic,payload))
        except:
            logging.warning ('Unable to convert payload to integer property message {}, payload is {}'.format(topic,payload))

 