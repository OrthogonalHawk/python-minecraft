import logging

class McStairOrientation(object):

    EAST = 0
    WEST = 1
    SOUTH = 2
    NORTH = 3

    def __init__(self):
        logging.error("This class doesn't do anything...")

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
    FARMLAND = 60
    FIRE = 51
    FLOWING_WATER = 8
    GRASS = 2
    OAK_DOOR_BLOCK = 64
    OAK_FENCE = 85
    OAK_FENCE_GATE = 107
    STILL_WATER = 9
    STONE = 1
    STONE_BRICK_STAIRS = 109
    TORCH = 50
    
    def __init__(self):
        logging.error("This class doesn't do anything...")
