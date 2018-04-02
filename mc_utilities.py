import time
import logging

class Location(object):

    def __init__(self, x, y, z, name):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

class McApiEvent(object):

    MODIFY_BLOCK = 0
    
    def __init__(self, type):
        self.type = type
        
class McApiSetBlockEvent(McApiEvent):

    def __init__(self, x, y, z, block_id):
        McApiEvent.__init__(self, McApiEvent.MODIFY_BLOCK)
        self.x = x
        self.y = y
        self.z = z
        self.block_id = block_id
        
    def get_location(self):
        return Location(x, y, z, "set_block_event")

class McApiEventRunner(object):

    def __init__(self, mc_api_events):
        self.events = list(mc_api_events)
    
    def run_events(self, mc_reference, initial_delay):
        
        # wait before running events
        time.sleep(initial_delay)
        
        # run all events
        num_events_run = 0
        for event in self.events:
            
            if event.type == McApiEvent.MODIFY_BLOCK:
            
                mc_reference.setBlock(event.x, event.y, event.z, event.block_id)
                num_events_run += 1
                
                logging.debug("Completed MODIFY_BLOCK event... (%u/%u)" % (num_events_run, len(self.events)))
                
            else:
                logging.error("Unsupported event.type %u" % (event.type))

class McApiBuilder(object):

    def __init__(self, building_name):
        self.name = building_name
        self.build_steps = []
        
    def _get_build_events(self):
        return self.build_steps
        
    def build(self, mc_reference):
        logging.info("Building %s" % (self.name))
        
        event_runner = McApiEventRunner(self._get_build_events())
        event_runner.run_events(mc_reference, 0)