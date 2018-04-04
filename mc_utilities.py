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
        self.final_build_steps = []
        self.anchor_corner = None
        
    def __init__(self, building_name, anchor_corner):
        self.name = building_name
        self.build_steps = []
        self.final_build_steps = []
        self.anchor_corner = anchor_corner
        
    def _get_start_stop_idx(self, pos_a, pos_b, dim):
        """Given two Locations and a dimension in [0,2] sort the corresponding
            coordinate values and return min, max."""
        start_idx, stop_idx = None, None
        
        if dim == 0:
            if pos_a.x < pos_b.x:
                start_idx = pos_a.x; stop_idx = pos_b.x
            else:
                start_idx = pos_b.x; stop_idx = pos_a.x
        
        elif dim == 1:
            if pos_a.y < pos_b.y:
                start_idx = pos_a.y; stop_idx = pos_b.y
            else:
                start_idx = pos_b.y; stop_idx = pos_a.y
                
        else:
            if pos_a.z < pos_b.z:
                start_idx = pos_a.z; stop_idx = pos_b.z
            else:
                start_idx = pos_b.z; stop_idx = pos_a.z
        
        # add 1 to stop index to fill in the last square
        #  otherwise it leaves a gap...
        return start_idx, stop_idx + 1
    
    def _add_block(self, pos_a, block_type, final_build_steps = False):
        if not final_build_steps:
            self.build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, pos_a.z, block_type))
        else:
            self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, pos_a.z, block_type))
    
    def _add_blocks_in_line(self, pos_a, pos_b, block_type, final_build_steps = False):
        
        if pos_a.x != pos_b.x and (pos_a.y == pos_b.y and pos_a.z == pos_b.z):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 0)
                
            for x_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(x_idx, pos_a.y, pos_a.z, block_type))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(x_idx, pos_a.y, pos_a.z, block_type))
    
        if pos_a.y != pos_b.y and (pos_a.x == pos_b.x and pos_a.z == pos_b.z):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 1)
            
            for y_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(pos_a.x, y_idx, pos_a.z, block_type))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, y_idx, pos_a.z, block_type))
            
        if pos_a.z != pos_b.z and (pos_a.x == pos_b.x and pos_a.y == pos_b.y):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 2)
        
            for z_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, z_idx, block_type))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, z_idx, block_type))
            
    def _get_build_events(self):
        return self.build_steps
        
    def _get_final_build_events(self):
        return self.final_build_steps
        
    def build(self, mc_reference):
        logging.info("Building %s" % (self.name))
        
        # add the basic build steps; fine if they occur in any order
        event_runner = McApiEventRunner(self._get_build_events())
        event_runner.run_events(mc_reference, 0)
        
        # now add any final build steps; guaranteed to occur last and
        #  in the order they were added to final_build_steps
        event_runner = McApiEventRunner(self._get_final_build_events())
        event_runner.run_events(mc_reference, 0)
        