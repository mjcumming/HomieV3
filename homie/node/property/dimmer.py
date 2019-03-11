from .property_integer import Property_Integer

class Dimmer(Property_Integer):

    def __init__(self, id='switch', name = 'Switch', settable = True, retained = True, qos=1, unit = None, data_type= 'enum', data_format = '0:100', value = None, callback=None):
        Property_Integer.__init__(self,id,name,settable,retained,qos,unit,data_type,data_format,value,callback)

 

