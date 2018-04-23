import logging

DEFAULT_BLOCK_STATE = 0

class McStairOrientation(object):

    EAST = 0
    WEST = 1
    SOUTH = 2
    NORTH = 3

    def __init__(self):
        logging.error("This class doesn't do anything...")

class McGlassColor(object):

    BLACK = 15
    BLUE = 11
    BROWN = 12
    CYAN = 9
    GRAY = 7
    GREEN = 13
    LIGHT_BLUE = 3
    LIGHT_GRAY = 8
    LIME = 5
    MAGENTA = 2
    ORANGE = 1
    PINK = 6
    PURPLE = 10
    RED = 14
    WHITE = DEFAULT_BLOCK_STATE
    YELLOW = 4
    
class McTorchOrientation(object):

    EAST = 1
    WEST = 2
    SOUTH = 3
    NORTH = 4

    def __init__(self):
        logging.error("This class doesn't do anything...")
        
class McBlockType(object):

    # definitions for the various kinds of MINECRAFT blocks
    AIR = 0
    DETECTOR_RAIL = 28
    PRISMARINE = 168
    FARMLAND = 60
    FIRE = 51
    FLOWING_WATER = 8
    GLASS = 95
    GRASS = 2
    OAK_DOOR_BLOCK = 64
    OAK_FENCE = 85
    OAK_FENCE_GATE = 107
    POWERED_RAIL = 27
    STILL_WATER = 9
    STONE = 1
    STONE_BRICK_STAIRS = 109
    TNT = 46
    TORCH = 50
    
    def __init__(self):
        logging.error("This class doesn't do anything...")
