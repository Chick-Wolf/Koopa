import math, random
from _sim import *

def run():
    if getTurn() == 0:
        (random.choice((cooperate,nothing,cheat)))()
    else:
        a = ['cooperate','nothing','cheat']
        a.remove(getAction(-1))
        act(random.choice(a))
