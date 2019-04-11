import PyISY
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

logger.debug('test')

# connect to ISY
isy = PyISY.ISY('192.168.1.213', 443, 'admin', 'admin', use_https=True, log=logger)
print(isy.connected)


def change_event_handler(event):
    print('Change Event {}'.format(event))

def control_event_handler(event):
    print('Control Event {}'.format(event))

#NODE = '49 A2 BE 1'
NODE = '42 C8 99 1'

node = isy.nodes[NODE]

change_handler=node.status.subscribe ('changed',change_event_handler)

control_handler=node.controlEvents.subscribe (control_event_handler)

isy.auto_update = True

while True:
    node.on()
    sleep(5)
    node.off()
    sleep(5)



'''
for (path, node) in isy.nodes:
    print('path {}, node {}'.format(path,node))
    #print('Node Name {}, type {}, dim {}, uom {}'.format(node.name,node.type,node.dimmable,node.uom))
'''

'''
for id in isy.nodes.nids:
    n = isy.nodes.getByID(id)
    print(n.name,n.__class__.__name__)
'''

