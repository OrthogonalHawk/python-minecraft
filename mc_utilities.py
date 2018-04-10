import constants
import copy
import logging
import random
import time

class Location(object):
        
    def __init__(self, x, y, z, name="unknown"):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        
    def __str__(self):
        return "(%u, %u, %u)" % (self.x, self.y, self.z)

    def update(self, modification):
        if len(modification) == 3:
            self.update_x(modification[0])
            self.update_y(modification[1])
            self.update_z(modification[2])
       
    def update_x(self, modification):
        self.x += modification
        
    def update_y(self, modification):
        self.y += modification
        
    def update_z(self, modification):
        self.z += modification
        
    def get_offset(self, modification):
        if len(modification) == 3:
            return Location(self.x + modification[0], self.y + modification[1], self.z + modification[2])
            
        else:
            return None

class McApiEvent(object):

    MODIFY_BLOCK = 0
    
    def __init__(self, type):
        self.type = type
        
class McApiSetBlockEvent(McApiEvent):

    def __init__(self, x, y, z, block_id, block_state):
        McApiEvent.__init__(self, McApiEvent.MODIFY_BLOCK)
        self.x = x
        self.y = y
        self.z = z
        self.block_id = block_id
        self.block_state = block_state
        
    def get_location(self):
        return Location(x, y, z, "set_block_event")

    def update_block_state_from_rotation(self, num_degrees):
        if self.block_id in [constants.McBlockType.STONE_BRICK_STAIRS]:
        
            if self.block_state == constants.McBlockOrientation.EAST:
                if num_degrees == 90:
                    self.block_state = constants.McBlockOrientation.NORTH
                elif num_degrees == 180:
                    self.block_state = constants.McBlockOrientation.WEST
                elif num_degrees == 270:
                    self.block_state = constants.McBlockOrientation.SOUTH
        
            elif self.block_state == constants.McBlockOrientation.WEST:
                if num_degrees == 90:
                    self.block_state = constants.McBlockOrientation.SOUTH
                elif num_degrees == 180:
                    self.block_state = constants.McBlockOrientation.EAST
                elif num_degrees == 270:
                    self.block_state = constants.McBlockOrientation.NORTH
                    
            elif self.block_state == constants.McBlockOrientation.SOUTH:
                if num_degrees == 90:
                    self.block_state = constants.McBlockOrientation.EAST
                elif num_degrees == 180:
                    self.block_state = constants.McBlockOrientation.NORTH
                elif num_degrees == 270:
                    self.block_state = constants.McBlockOrientation.WEST
            
            elif self.block_state == constants.McBlockOrientation.NORTH:
                if num_degrees == 90:
                    self.block_state = constants.McBlockOrientation.WEST
                elif num_degrees == 180:
                    self.block_state = constants.McBlockOrientation.SOUTH
                elif num_degrees == 270:
                    self.block_state = constants.McBlockOrientation.EAST
                    
class McApiEventRunner(object):

    ANIMATION_DELAY = 0.01
    
    def __init__(self, mc_api_events):
        self.events = list(mc_api_events)
    
    def run_events(self, mc_reference, initial_delay, animate = False):
        
        # wait before running events
        time.sleep(initial_delay)
        
        # run all events
        num_events_run = 0
        random.shuffle(self.events)
                
        for event in self.events:
            
            if event.type == McApiEvent.MODIFY_BLOCK:
            
                mc_reference.setBlock(event.x, event.y, event.z, event.block_id, event.block_state)
                num_events_run += 1
                
                logging.debug("Completed MODIFY_BLOCK event... (%u/%u)" % (num_events_run, len(self.events)))
                
                # create a simple animation effect if requested
                if animate:
                    time.sleep(self.ANIMATION_DELAY)
                    
            else:
                logging.error("Unsupported event.type %u" % (event.type))

class McApiBuilder(object):

    DEFAULT_BLOCK_STATE = 0

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
        
    def __str__(self):
        return "%s at %s" % (self.NAME, self.anchor_corner)
        
    def _get_build_corners(self, anchor_corner, x_dim, z_dim):
        corners = []
        
        if anchor_corner != None:
            # create four copies of the anchor corner
            for i in range(4):
                corners.append(copy.deepcopy(anchor_corner))
            
            # update the corners with the building dimensions
            corners[1].update([x_dim, 0, 0])
            corners[2].update([x_dim, 0, -z_dim])
            corners[3].update([0,     0, -z_dim])
        
        return corners
        
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
        
    def _add_block(self, pos_a, block_type, block_state=DEFAULT_BLOCK_STATE, final_build_steps=False):          
        if not final_build_steps:
            self.build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, pos_a.z, block_type, block_state))
        else:
            self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, pos_a.z, block_type, block_state))
    
    def _add_blocks_in_line(self, pos_a, pos_b, block_type, final_build_steps = False):
        
        if pos_a.x != pos_b.x and (pos_a.y == pos_b.y and pos_a.z == pos_b.z):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 0)
                
            for x_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(x_idx, pos_a.y, pos_a.z, block_type, self.DEFAULT_BLOCK_STATE))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(x_idx, pos_a.y, pos_a.z, block_type, self.DEFAULT_BLOCK_STATE))
    
        if pos_a.y != pos_b.y and (pos_a.x == pos_b.x and pos_a.z == pos_b.z):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 1)
            
            for y_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(pos_a.x, y_idx, pos_a.z, block_type, self.DEFAULT_BLOCK_STATE))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, y_idx, pos_a.z, block_type, self.DEFAULT_BLOCK_STATE))
            
        if pos_a.z != pos_b.z and (pos_a.x == pos_b.x and pos_a.y == pos_b.y):
            start_idx, stop_idx = self._get_start_stop_idx(pos_a, pos_b, 2)
        
            for z_idx in range(start_idx, stop_idx):
                if not final_build_steps:
                    self.build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, z_idx, block_type, self.DEFAULT_BLOCK_STATE))
                else:
                    self.final_build_steps.append(McApiSetBlockEvent(pos_a.x, pos_a.y, z_idx, block_type, self.DEFAULT_BLOCK_STATE))
    
    def _add_blocks_in_cubeoid(self, pos_a, pos_b, block_type, final_build_steps = False):
        """Alternate function to mcpi.minecraft setBlocks; allows the base class to track all
            blocks added for a structure."""
        x_start_idx, x_stop_idx = self._get_start_stop_idx(pos_a, pos_b, 0)
        y_start_idx, y_stop_idx = self._get_start_stop_idx(pos_a, pos_b, 1)
        z_start_idx, z_stop_idx = self._get_start_stop_idx(pos_a, pos_b, 2)
        
        for x_idx in range(x_start_idx, x_stop_idx):
            for y_idx in range(y_start_idx, y_stop_idx):
                for z_idx in range(z_start_idx, z_stop_idx):
                    if not final_build_steps:
                        self.build_steps.append(McApiSetBlockEvent(x_idx, y_idx, z_idx, block_type, self.DEFAULT_BLOCK_STATE))
                    else:
                        self.final_build_steps.append(McApiSetBlockEvent(x_idx, y_idx, z_idx, block_type, self.DEFAULT_BLOCK_STATE))
        
    def _add_build_steps(self, new_build_steps, final_build_steps = False):
        if not final_build_steps:
            self.build_steps += copy.deepcopy(new_build_steps)
        else:
            self.final_build_steps += copy.deepcopy(new_build_steps)
            
    def _get_build_events(self):
        return self.build_steps
        
    def _get_final_build_events(self):
        return self.final_build_steps
        
    def _get_rotation_point(self):
        rot_x, rot_z = None, None
        for step in self.build_steps + self.final_build_steps:
            if rot_x == None and rot_z == None:
                rot_x = step.x
                rot_z = step.z
                continue
            
            if step.x < rot_x:
                rot_x = step.x
            
            if step.z > rot_z:
                rot_z = step.z
                
        return rot_x, rot_z
        
    def build(self, mc_reference, animate = False):
        logging.info("Building %s" % (self.name))
        
        # add the basic build steps; fine if they occur in any order
        event_runner = McApiEventRunner(self._get_build_events())
        event_runner.run_events(mc_reference, 0, animate)
        
        # now add any final build steps; guaranteed to occur last and
        #  in the order they were added to final_build_steps
        event_runner = McApiEventRunner(self._get_final_build_events())
        event_runner.run_events(mc_reference, 0, animate)
    
    def rotate(self, num_degrees):
        num_degrees %= 360
        if num_degrees in [90, 180, 270]:
        
            rot_origin_x, rot_origin_z = self._get_rotation_point()
            
            for step in self.build_steps + self.final_build_steps:
                
                # to make the math easier, convert between the original Minecraft
                #  coordinate system and one where the origin is now at the rotation
                #  point for this object.
                origin_at_rot_x = step.x - rot_origin_x
                origin_at_rot_z = step.z - rot_origin_z
                
                # rotate each block independently, taking Minecraft's coordinate
                #  system into account (different that traditional X-Y system)
                if num_degrees == 90:
                    step.x = origin_at_rot_z + rot_origin_x
                    step.z = -origin_at_rot_x + rot_origin_z
                                        
                elif num_degrees == 180:
                    step.x = -origin_at_rot_x + rot_origin_x
                    step.z = -origin_at_rot_z + rot_origin_z
                    
                elif num_degrees == 270:
                    step.x = -origin_at_rot_z + rot_origin_x
                    step.z = origin_at_rot_x + rot_origin_z
                    
                else:
                    logging.error("Unsupported rotation %u" % (num_degrees))
            
                # update block state if necessary for rotation
                step.update_block_state_from_rotation(num_degrees)
                
        else:
            logging.error("Unable to rotate %u degrees" % (num_degrees))
    
    def update_anchor(self, modification):
        for step in self.build_steps + self.final_build_steps:
            if len(modification) == 3:
                step.x += modification[0]
                step.y += modification[1]
                step.z += modification[2]
        
        