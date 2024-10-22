"""
Reasonable, tries to win this with the opponent. If not possible to cooperate, decide to do nothing.
"""

import math, random
from _sim import *

def run():
    if getTurn() == 0:
        nothing()
    else:
        act({
            'cooperate': 'cooperate',
            'nothing': 'nothing',
            'cheat': 'nothing',
        }[getAction(-1)])
