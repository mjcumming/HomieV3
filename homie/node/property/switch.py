from .property_enum import Property_Enum

class Switch(Property_Enum):

    def __init__(self, id='switch', name = 'Switch', settable = True, retained = True, qos=1, unit = None, data_type= 'enum', data_format = 'ON,OFF', value = None, callback=None):
        Property_Enum.__init__(self,id,name,settable,retained,qos,unit,data_type,data_format,value,callback)

 

if __name__ == '__main__':
    np = Switch ('x','x')