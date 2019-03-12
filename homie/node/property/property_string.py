import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Property_String(Property_Base):

    def __init__(self, id, name, settable=False, retained=True, qos=1, unit=None, data_type='string', data_format=None, value=None, set_value=None):
        super().__init__(id,name,settable,retained,qos,unit,'string',data_format,value,set_value)


