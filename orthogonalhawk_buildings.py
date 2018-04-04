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
    STACK_SPACING = 4
    
    def __init__(self, anchor_corner, x_dim, z_dim, num_stacks):
        BasicFarm.__init__(self, anchor_corner, x_dim, z_dim)
        
        for i in range(num_stacks - 1):
            self._create_farm(mc_utilities.Location(anchor_corner.x, anchor_corner.y + self.STACK_SPACING * (i + 1), anchor_corner.z), x_dim, z_dim)
            