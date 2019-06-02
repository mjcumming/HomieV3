import time
from threading import Event, Thread

import logging

logger = logging.getLogger(__name__)

class Repeating_Timer (object):

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval):
        self.interval = interval

        self.start = time.time()
        self.event = Event()

        self.thread = Thread(target=self._target)
        self.thread.setDaemon(True)
        self.thread.start()

        self.callbacks = []

    def _target(self):
        while not self.event.wait(self._time):
            for callback in self.callbacks:
                try:
                    callback ()
                except Exception as e:
                    logger.warning ('Error in timer callback: {}'.format(e))

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def add_callback(self,callback):
        self.callbacks.append(callback)

    def stop(self):
        self.event.set()
        self.thread.join()

def printme ():
    print ('me')
def printyou ():
    print ('you')
def printerr ():
    print (10/0)


if __name__ == "__main__":

    rt = Repeating_Timer(6)

    rt.add_callback(printme)
    rt.add_callback(printyou)
    rt.add_callback(printerr)
 
    #while True:
    time.sleep (20)
     #   pass
