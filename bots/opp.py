import math, random
from _sim import *

def run():
    if getTurn() == 0:
        nothing()
    else:
        act({
            'cooperate': 'cooperate',
            'nothing': 'cooperate',
            'cheat': 'nothing',
        }[getAction(-1)])
