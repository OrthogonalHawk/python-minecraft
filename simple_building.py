import argparse
import logging
from mcpi.minecraft import Minecraft
import mc_utilities
import orthogonalhawk_buildings
import time

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# create a reference to the game
mc = Minecraft.create()

base_corner = mc_utilities.Location(455, 63, 44, "base_corner")

# create the structure
my_building = orthogonalhawk_buildings.BasicFarm(base_corner, 9, 9)
time.sleep(5)
my_building.build(mc)

#print(mc.player.getTilePos()) # 469, 43, 30
#mc.player.setTilePos(454, 63, 44)