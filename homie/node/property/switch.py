from .property_base import Property_Base

class Switch(Property_Base):

    def __init__(self, id='switch', name = 'Switch', settable = True, retained = True, unit = None, data_type= 'enum', data_format = 'ON,OFF', value = None):
        Property_Base.__init__(self,id,name,settable,retained,unit,data_type,data_format,value)


if __name__ == '__main__':
    np = Switch ('x','x')