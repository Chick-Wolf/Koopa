from typing import Literal, Union

import math, random
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

import _sim

Action = Union[Literal['cooperate'], Literal['nothing'], Literal['cheat']]

PLAYER_NAME = ('A','B')
PLAYER_NAME_COLOR = ('\x1b[91mA\x1b[39m','\x1b[94mB\x1b[39m')

def get_scores_util(a: Action, b: Action) -> int:
    return {
        ('cooperate','cooperate') : 2,
        ('cooperate','nothing') : -1,
        ('cooperate','cheat') : -1,
        
        ('nothing','cooperate') : 3,
        ('nothing','nothing') : 0,
        ('nothing','cheat') : 0,
        
        ('cheat','cooperate') : 4,
        ('cheat','nothing') : -2,
        ('cheat','cheat') : -2,
    }[(a,b)]

def get_scores(a: Action, b: Action) -> tuple[int,int]:
    return (get_scores_util(a,b),get_scores_util(b,a))

def color_gain(n: int) -> str:
    if n == 0:
        return '\x1b[33m~%d\x1b[39m'%(n,)
    c = '32' if n > 0 else '31'
    return '\x1b[%sm%+d\x1b[39m'%(c,n)

def color_act(act: Action) -> str:
    return {
        'cooperate': '\x1b[32mC\x1b[39m',
        'nothing': '\x1b[33mN\x1b[39m',
        'cheat': '\x1b[31mT\x1b[39m',
    }[act]
    

def play_round():
    actions_a: list[str] = []
    actions_b: list[str] = []
    
    act_a: str = None
    act_b: str = None

    player: Union[Literal[0],Literal[1]] = 0
    
    score_a: int = 0
    score_b: int = 0

    def act( action: Action ) -> None:
        nonlocal act_a, act_b
        
        if action not in ('cooperate', 'nothing', 'cheat'):
            raise TypeError('Bad action %s, expected one of "cooperate", "nothing", "cheat"'%(repr(action),))
        
        if player == 0:
            act_a = action
        else:
            act_b = action

    def cooperate() -> None:
        act('cooperate')

    def nothing() -> None:
        act('nothing')

    def cheat() -> None:
        act('cheat')
        
    def getAction(n: int) -> Action:
        return (actions_a,actions_b)[player][n]
    
    def getSelf(n: int) -> Action:
        return (actions_a,actions_b)[1-player][n]
        
    _sim.cooperate = cooperate
    _sim.nothing = nothing
    _sim.cheat = cheat
    _sim.act = act
    _sim.getAction = getAction
    _sim.getSelf = getSelf
    _sim.getTurn = lambda: i_turn
    
    bot_path = str(Path('bot.py').absolute())
    
    spec = spec_from_file_location('bot', bot_path)
    
    bot_a = module_from_spec(spec)
    spec.loader.exec_module(bot_a)
    
    bot_b = module_from_spec(spec)
    spec.loader.exec_module(bot_b)

    for i_turn in range(10):        
        act_a = act_b = None
        
        for pl, run in ( (0,bot_a.run), (1,bot_b.run) ):
            player = pl
            try:
                run()
            except BaseException as ex:
                print('Player %s has \x1b[91;1mcrashded\x1b[39;22m: \x1b[90m(during turn #%d)\x1b[39m'%(PLAYER_NAME_COLOR[pl],i_turn+1))
                print(ex)
                exit(1)
        
        np = (['A'] if not act_a else []) + (['B'] if not act_b else [])
        
        if len(np):
            plur = 's' if len(np) != 1 else ''
            plur2 = 'ont' if len(np) != 1 else 'a'
            print('Le%s joueur%s %s n\'%s pas choisi'%(plur,plur,' et '.join(np),plur2))
            exit(1)
            
        sa, sb = get_scores(act_a,act_b)
        
        score_a += sa
        score_b += sb
        
        print('╭── turn %02d ───╮'%(i_turn+1,))
        print('│ \x1b[91mA\x1b[39m: %2d \x1b[90m(%s\x1b[90m)\x1b[39m %s │'%(score_a,color_gain(sa),color_act(act_a)))
        print('│ \x1b[94mB\x1b[39m: %2d \x1b[90m(%s\x1b[90m)\x1b[39m %s │'%(score_b,color_gain(sb),color_act(act_b)))
        print('╰──────────────╯')
        
        actions_a.append(act_a)
        actions_b.append(act_b)

play_round()
