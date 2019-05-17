
from homie.support.helpers import validate_id

# Ndee arrays not implemented


class Node_Base(object):

    def __init__(self, device, id, name, type_, retain=True, qos=1):
        assert validate_id(id)
        assert device
        self.id = id
        self.name = name
        self.type = type_
        self.device = device

        self.retain = retain
        self.qos = qos

        self.properties = {}

        self.topic = self.device.topic

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, parent_topic):
        self._topic =  "/".join([parent_topic,self.id])

    def add_property(self, property_):
        #assert self.properties [property_.id] == None
        self.properties [property_.id] = property_

        if self.device.start_time is not None: #running, publish property changes
            self.publish_properties()

    def remove_property(self, property_id):
        del self.properties [property_id]

        if self.device.start_time is not None: #running, publish property changes
            self.publish_properties()

    def get_property(self, property_id):
        if property_id in self.properties:
            return self.properties [property_id]
        else:
            return None

    def set_property_value(self, property_id, value):
        self.get_property (property_id).value = value

    def publish(self,topic,payload,retain,qos):
        self.device.publish (topic,payload,retain,qos)

    def publish_attributes(self):
        self.publish ("/".join((self.topic, "$name")), self.name, self.retain, self.qos)
        self.publish ("/".join((self.topic, "$type")), self.type, self.retain, self.qos)

        self.publish_properties()
        
    def publish_properties(self):
        properties = ",".join(self.properties.keys())
        self.publish ("/".join((self.topic, "$properties")), properties, True, 1)

        for _,property_ in self.properties.items():
            property_.publish_attributes()        

    def get_subscriptions(self):
        subscriptions = {}
        
        for _,property_ in self.properties.items():
            subscriptions.update (property_.get_subscriptions())

        return subscriptions

