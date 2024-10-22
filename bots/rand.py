"""
Picks a random action each turn
"""

import math, random
from _sim import *

def run():
    (random.choice((cooperate,nothing,cheat)))()
