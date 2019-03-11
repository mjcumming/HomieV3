
from helpers import validate_id

# Arrays not implemented


class Node_Base(object):

    def __init__(self, id, name, type_):
        assert validate_id(id)
        self.id = id
        self.name = name
        self.type = type_

        self.properties = {}

        self.parent_publisher = None

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, parent_topic):
        self._topic =  "/".join([parent_topic,self.id])

    def add_property(self, property_):
        self.properties [property_.id] = property_
        property_.topic = self.topic
        property_.parent_publisher = self.parent_publisher

    def publish(self,topic,payload,retain,qos):
        self.parent_publisher (topic,payload)

    def publish_attributes(self):
        self.publish ("/".join((self.topic, "$name")), self.name, True, 1)
        self.publish ("/".join((self.topic, "$type")), self.type, True, 1)

        self.publish_properties()
        
    def publish_properties(self):
        properties = ",".join(self.properties.keys())
        self.publish ("/".join((self.topic, "$properties")), properties, True, 1)

        for _,property_ in self.properties.items():
            property_.publish_attributes()        

    def get_subscriptions(self):
        subscriptions = {}
        
        for id,property_ in self.properties.items():
            subscriptions.update (property_.get_subscriptions())

        return subscriptions

