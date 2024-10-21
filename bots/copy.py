import math, random
from _sim import *

def run():
    if getTurn() == 0:
        (random.choice((cooperate,nothing,cheat)))()
    else:
        act(getAction(-1))
