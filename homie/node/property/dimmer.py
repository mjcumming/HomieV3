from .property_integer import Property_Integer

class Dimmer(Property_Integer):

    def __init__(self, id='dimmer', name = 'Dimmer', settable = True, retained = True, qos=1, unit = '%', data_type= None, data_format = '0:100', value = None, callback=None):
        super().__init__(id,name,settable,retained,qos,unit,data_type,data_format,value,callback)

 

