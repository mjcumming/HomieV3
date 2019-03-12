from .property_enum import Property_Enum

class Switch(Property_Enum):

    def __init__(self, id='contact', name = 'Contact', settable = False, retained = True, qos=1, unit = None, data_type= 'enum', data_format = 'OPEN,CLOSED', value = None, set_value=None):
        
        super().__init__(id,name,settable,retained,qos,unit,data_type,data_format,value,set_value)

 

