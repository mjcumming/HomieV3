from .property_integer import Property_Integer

class Property_Dimmer(Property_Integer):

    def __init__(self,node, id='dimmer', name = 'Dimmer', settable = True, retained = True, qos=1, unit = '%', data_type= None, data_format = '0:100', value = None, set_value=None):
        
        super().__init__(node,id,name,settable,retained,qos,unit,data_type,data_format,value,set_value)

 

