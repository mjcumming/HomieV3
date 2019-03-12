from .property_float import Property_Float

class Temperature_Property(Property_Float):

    def __init__(self, id='temperature', name = 'Temperature', settable = False, retained = True, qos=1, unit = None, data_type= None, data_format = None, value = None, callback=None):
        
        super().__init__(id,name,settable,retained,qos,unit,data_type,data_format,value,callback)

 

