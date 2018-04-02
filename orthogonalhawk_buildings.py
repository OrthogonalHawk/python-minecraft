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
    
    BORDER_WIDTH = 2
    
    def __init__(self, anchor_corner, x_dim, z_dim):
        mc_utilities.McApiBuilder.__init__(self, "basic_farm", anchor_corner)
        
        # define the outer fence corners
        corner_01, corner_02, corner_03, corner_04 = copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner), copy.deepcopy(anchor_corner)
        corner_02.x += x_dim
        corner_03.x += x_dim; corner_03.z += z_dim
        corner_04.z += z_dim
        
        logging.info("Defined corners: (%u, %u), (%u, %u), (%u, %u), (%u, %u)" %
            (corner_01.x, corner_01.z, corner_02.x, corner_02.z,
             corner_03.x, corner_03.z, corner_04.x, corner_04.z))
        
        self._add_blocks_in_line(corner_01, corner_02, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_02, corner_03, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_03, corner_04, constants.McBlockType.OAK_FENCE)
        self._add_blocks_in_line(corner_04, corner_01, constants.McBlockType.OAK_FENCE)
        
        
        