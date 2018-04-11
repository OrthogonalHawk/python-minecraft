import constants
import copy
import logging
import mc_utilities

class SimpleBuilding(mc_utilities.McApiBuilder):

    def __init__(self, anchor_corner):
        mc_utilities.McApiBuilder.__init__(self, "my_first_building")
        self.anchor_corner = anchor_corner
        
        # define the structure
        for x_idx in range(self.anchor_corner.x, self.anchor_corner.x + 10):
            self.build_steps.append(mc_utilities.McApiSetBlockEvent(x_idx, anchor_corner.y, anchor_corner.z, 103))

class BasicFarm(mc_utilities.McApiBuilder):
    
    BORDER_WIDTH = 1
    NAME = "BasicFarm"
    
    def __init__(self, anchor_corner, x_dim, z_dim):
        mc_utilities.McApiBuilder.__init__(self, self.NAME, anchor_corner)
        self._create_farm(anchor_corner, x_dim, z_dim)
        
    def _create_farm(self, anchor_corner, x_dim, z_dim):
     
        logging.info("Building %s with anchor_corner=(%u, %u, %u) and dimensions (%u, %u)" %
            (self.NAME, anchor_corner.x, anchor_corner.y, anchor_corner.z,
             x_dim, z_dim))
    
        # define the outer fence corners
        corner_01, corner_02, corner_03, corner_04 = copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner)
        corner_02.x += x_dim + self.BORDER_WIDTH
        corner_03.x += x_dim + self.BORDER_WIDTH; corner_03.z += z_dim + self.BORDER_WIDTH
        corner_04.z += z_dim + self.BORDER_WIDTH
        
        logging.info("Defined corners: (x,z) (%u, %u), (%u, %u), (%u, %u), (%u, %u)" %
            (corner_01.x, corner_01.z, corner_02.x, corner_02.z,
             corner_03.x, corner_03.z, corner_04.x, corner_04.z))
        
        # define gate positions
        gate_01 = mc_utilities.Location(corner_01.x + (x_dim + self.BORDER_WIDTH) / 2, corner_01.y, corner_01.z, "%s_gate_01" % (self.NAME))
        gate_02 = mc_utilities.Location(corner_04.x + (x_dim + self.BORDER_WIDTH) / 2, corner_04.y, corner_04.z, "%s_gate_01" % (self.NAME))
        
        logging.info("Defined gates:   (x,z) (%u, %u), (%u, %u)" %
            (gate_01.x, gate_01.z, gate_02.x, gate_02.z))
        
        # clear the above ground farm area
        self._add_blocks_in_cubeoid(corner_01, corner_03, constants.McBlockType.AIR)
        
        # add the fence lines
        self._add_blocks_in_line(corner_01, corner_02, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_02, corner_03, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_03, corner_04, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_04, corner_01, constants.McBlockType.OAK_FENCE)
        
        # add gates on each side of the fence; make sure that these are in the final_build_steps
        #  because they need to override the previously constructed fence lines.
        self._add_block(gate_01, constants.McBlockType.OAK_FENCE_GATE, True)
        self._add_block(gate_02, constants.McBlockType.OAK_FENCE_GATE, True)
        
        # add torches at each corner
        self._add_block(mc_utilities.Location(corner_01.x, corner_01.y + 1, corner_01.z), constants.McBlockType.TORCH, True)
        self._add_block(mc_utilities.Location(corner_02.x, corner_02.y + 1, corner_02.z), constants.McBlockType.TORCH, True)
        self._add_block(mc_utilities.Location(corner_03.x, corner_03.y + 1, corner_03.z), constants.McBlockType.TORCH, True)
        self._add_block(mc_utilities.Location(corner_04.x, corner_04.y + 1, corner_04.z), constants.McBlockType.TORCH, True)
        
        # update corners to that they are now under the fence
        corner_01.y -= 1; corner_02.y -= 1; corner_03.y -= 1; corner_04.y -= 1
        self._add_blocks_in_line(corner_01, corner_02, constants.McBlockType.GRASS)
        self._add_blocks_in_line(corner_02, corner_03, constants.McBlockType.GRASS)
        self._add_blocks_in_line(corner_03, corner_04, constants.McBlockType.GRASS)
        self._add_blocks_in_line(corner_04, corner_01, constants.McBlockType.GRASS)
        
        # now add farmland inside the fence
        corner_01.x += self.BORDER_WIDTH; corner_01.z += self.BORDER_WIDTH
        corner_03.x -= self.BORDER_WIDTH; corner_03.z -= self.BORDER_WIDTH
        self._add_blocks_in_cubeoid(corner_01, corner_03, constants.McBlockType.FARMLAND)
        
        # add a water square so that the farm is irrigated
        self._add_block(mc_utilities.Location(gate_01.x, gate_01.y - 1, gate_01.z + (z_dim + self.BORDER_WIDTH)/ 2), constants.McBlockType.FLOWING_WATER)
        
class StackedFarm(BasicFarm):

    NAME = "StackedFarm"
    STACK_SPACING = 6
    
    def __init__(self, anchor_corner, x_dim, z_dim, num_stacks):
        BasicFarm.__init__(self, anchor_corner, x_dim, z_dim)
        
        for i in range(num_stacks - 1):
            self._create_farm(mc_utilities.Location(anchor_corner.x, anchor_corner.y + self.STACK_SPACING * (i + 1), anchor_corner.z), x_dim, z_dim)

class StairComponent(mc_utilities.McApiBuilder):

    NAME = "StairComponent"

    def __init__(self, anchor_corner):
        mc_utilities.McApiBuilder.__init__(self, self.NAME, anchor_corner)
        self._create_stair_component(anchor_corner)
        
    def _create_stair_component(self, anchor_corner):
    
        logging.info("Creating %s at %s" % (self.NAME, anchor_corner))
        
        # create the base structure
        self._add_blocks_in_cubeoid(anchor_corner.get_offset([0, -1, 0]), anchor_corner.get_offset([0, -1, -1]), constants.McBlockType.STONE)
    
        # add a torch
        self._add_block(anchor_corner.get_offset([1, -1, -1]), constants.McBlockType.TORCH, constants.McTorchOrientation.EAST, True)
        
        # create the stair part
        self._add_block(anchor_corner, constants.McBlockType.STONE_BRICK_STAIRS, constants.McStairOrientation.EAST, True)
        self._add_block(anchor_corner.get_offset([0, 0, -1]), constants.McBlockType.STONE_BRICK_STAIRS, constants.McStairOrientation.EAST, True)
        
        # add a raised flat part
        self._add_block(anchor_corner.get_offset([1, 0,  0]), constants.McBlockType.STONE)
        self._add_block(anchor_corner.get_offset([2, 0,  0]), constants.McBlockType.STONE)
        self._add_block(anchor_corner.get_offset([1, 0, -1]), constants.McBlockType.STONE)
        self._add_block(anchor_corner.get_offset([2, 0, -1]), constants.McBlockType.STONE)

class SpiralStairCase(mc_utilities.McApiBuilder):

    NAME = "SpiralStairCase"
    
    def __init__(self, anchor_corner, height):
        mc_utilities.McApiBuilder.__init__(self, self.NAME, anchor_corner)
        self._create_spiral_staircase(anchor_corner, height)
        
    def _create_spiral_staircase(self, anchor_corner, height):
        
        logging.info("Creating %s at %s" % (self.NAME, anchor_corner))
        
        anchor_updates = [ [2, 1, -2], [-1, 1, -1], [1, 1, 3], [4, 1, 0] ]
        
        stair_component_anchor = anchor_corner.get_offset([2, 0, 0])
        tmp_stair_component = StairComponent(stair_component_anchor)
        
        logging.info("%s" % (tmp_stair_component))
        
        # add the initial set of blocks
        self._add_build_steps(tmp_stair_component._get_build_events(), False)
        self._add_build_steps(tmp_stair_component._get_final_build_events(), True)
        
        component_rotation = 0
        for i in range(abs(height) - 1):
        
            # start by rotating the staircase component
            tmp_stair_component.rotate(90)
            
            # now update the anchor offset for the new location
            next_anchor_update = anchor_updates[component_rotation % len(anchor_updates)]
            if height < 0:
                next_anchor_update[1] = -1
            tmp_stair_component.update_anchor(next_anchor_update)
            
            # add the next set of blocks
            self._add_build_steps(tmp_stair_component._get_build_events(), False)
            self._add_build_steps(tmp_stair_component._get_final_build_events(), True)
    
            component_rotation += 1
            
class WatchTower(mc_utilities.McApiBuilder):

    NAME = "WatchTower"
    BASE_TOWER_DIM = 7
    STAIR_WIDTH = 2
    TOWER_HEIGHT = 20
    TOWER_WALL_WIDTH = 1
    
    def __init__(self, anchor_corner):
        mc_utilities.McApiBuilder.__init__(self, self.NAME, anchor_corner)
        self._create_watch_tower(anchor_corner)
        
    def _create_watch_tower(self, anchor_corner):
    
        logging.info("Building %s with anchor_corner=(%u, %u, %u)" %
            (self.NAME, anchor_corner.x, anchor_corner.y, anchor_corner.z))
        
        tower_corners = self._get_build_corners(anchor_corner, self.BASE_TOWER_DIM - 1, self.BASE_TOWER_DIM - 1)
        
        logging.info("Defined corners: (x,z) (%u, %u), (%u, %u), (%u, %u), (%u, %u)" %
            (tower_corners[0].x, tower_corners[0].z, tower_corners[1].x, tower_corners[1].z,
             tower_corners[2].x, tower_corners[2].z, tower_corners[3].x, tower_corners[3].z))
             
        # create the outer tower shell
        for y_idx in range(self.TOWER_HEIGHT):
            self._add_blocks_in_line(tower_corners[0].get_offset([0, y_idx, 0]), tower_corners[1].get_offset([0, y_idx, 0]), constants.McBlockType.STONE)
            self._add_blocks_in_line(tower_corners[1].get_offset([0, y_idx, 0]), tower_corners[2].get_offset([0, y_idx, 0]), constants.McBlockType.STONE)
            self._add_blocks_in_line(tower_corners[2].get_offset([0, y_idx, 0]), tower_corners[3].get_offset([0, y_idx, 0]), constants.McBlockType.STONE)
            self._add_blocks_in_line(tower_corners[3].get_offset([0, y_idx, 0]), tower_corners[0].get_offset([0, y_idx, 0]), constants.McBlockType.STONE)
        
        # create the tower floor
        self._add_blocks_in_cubeoid(tower_corners[0].get_offset([0, -1, 0]), tower_corners[2].get_offset([0, -1, 0]), constants.McBlockType.STONE)
        
        # create the inner column
        tower_center_at_base = tower_corners[0].get_offset([3, 0, -3])
        self._add_blocks_in_line(tower_center_at_base, tower_center_at_base.get_offset([0, self.TOWER_HEIGHT-1, 0]), constants.McBlockType.STONE)
        
        logging.info("Tower center at %s" % (tower_center_at_base))
        
        # create the inner staircase using SpiralStairCase
        spiral_staircase = SpiralStairCase(tower_corners[0].get_offset([1, 0, -1]), self.TOWER_HEIGHT)
        self._add_build_steps(spiral_staircase._get_build_events(), False)
        self._add_build_steps(spiral_staircase._get_final_build_events(), True)
        
        
        #stair_case_block_pos = tower_center_at_base.get_offset([0, -1, 1])
        #logging.info("Staircase start position: %s" % (stair_case_block_pos))
        
        
        
        #next_stair_offset = [ [1, 1, 0], [1, 1, 0], [0, 1, -1], [0, 1, -1], [-1, 1, 0], [-1, 1, 0], [0, 1, 1], [0, 1, 1] ]
        #next_stair_offset_ctr = 1
        #for y_idx in range(self.TOWER_HEIGHT):
            
            # advance to the next staircase position            
            #stair_case_block_pos.update(next_stair_offset[next_stair_offset_ctr])
            #next_stair_offset_ctr += 1
            #next_stair_offset_ctr %= len(next_stair_offset)
            
            #logging.info("Adding stairs at %s" % (stair_case_block_pos))
            
            #self._add_block(stair_case_block_pos, constants.McBlockType.STONE_BRICK_STAIRS)        
        