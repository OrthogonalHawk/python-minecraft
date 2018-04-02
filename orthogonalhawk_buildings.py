import logging
import mc_utilities

class SimpleBuilding(mc_utilities.McApiBuilder):

    def __init__(self, anchor_corner):
        mc_utilities.McApiBuilder.__init__(self, "my_first_building")
        self.anchor_corner = anchor_corner
        
        # define the structure
        for x_idx in range(self.anchor_corner.x, self.anchor_corner.x + 10):
            self.build_steps.append(mc_utilities.McApiSetBlockEvent(x_idx, anchor_corner.y, anchor_corner.z, 103))
            