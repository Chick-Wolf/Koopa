from typing import Literal, Union

from importlib.util import spec_from_file_location, module_from_spec

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

class RoundResult:

    class Player:

        actions: list[Action]
        score:   int

        def __init__(self, actions: list[Action], score: int):
            self.actions = actions
            self.score = score

    a: Player
    b: Player

    def __init__(self, a: Player, b: Player):
        self.a = a
        self.b = b
        
class Bot:
    
    path: str
    func: str
    
    def __init__(self, path: str, func: str):
        self.path = path
        self.func = func

def play_round( a: Bot, b: Bot, debug: bool = False ) -> Union[RoundResult,None]:
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
    
    def getTurn() -> int:
        return i_turn
    
    def assign_funcs(obj):
        obj.cooperate = cooperate
        obj.nothing = nothing
        obj.cheat = cheat
        obj.act = act
        obj.getAction = getAction
        obj.getSelf = getSelf
        obj.getTurn = getTurn
        
    assign_funcs(_sim)

    spec_a = spec_from_file_location('bot_a',a.path)
    if not spec_a:
        print('Could not find file \x1b[95m%s\x1b[39m for bot %s'%(repr(a.path),PLAYER_NAME_COLOR[0]))
        return None
    bot_a = module_from_spec(spec_a)
    spec_a.loader.exec_module(bot_a)
    assign_funcs(bot_a)

    spec_b = spec_from_file_location('bot_b',b.path)
    if not spec_b:
        print('Could not find file \x1b[95m%s\x1b[39m for bot %s'%(repr(b.path),PLAYER_NAME_COLOR[1]))
        return None
    bot_b = module_from_spec(spec_b)
    spec_b.loader.exec_module(bot_b)
    assign_funcs(bot_b)

    for i_turn in range(10):
        act_a = act_b = None
        
        for pl, mod, bot in ( (0,bot_a,a), (1,bot_b,b) ):
            if not hasattr(mod, bot.func):
                print('\x1b[90m(during turn #%d)\x1b[39m'%(i_turn+1,))
                print('Could not find \x1b[95m%s\x1b[39m in bot %s'%(repr(bot.func),PLAYER_NAME_COLOR[pl]))
                return None

        for pl, run in ( (0,getattr(bot_a,a.func)), (1,getattr(bot_b,b.func)) ):
            player = pl
            try:
                run()
            except BaseException as ex:
                print('\x1b[90m(during turn #%d)\x1b[39m'%(i_turn+1,))
                print('Player %s has \x1b[91;1mcrashded\x1b[39;22m:'%(PLAYER_NAME_COLOR[pl]))
                print(ex)
                return None

        np = (['A'] if not act_a else []) + (['B'] if not act_b else [])

        if len(np):
            plur = 's' if len(np) != 1 else ''
            print('\x1b[90m(during turn #%d)\x1b[39m'%(i_turn+1,))
            print('Player%s %s didn\'t choose'%(plur,' and '.join(np)))
            return None

        sa, sb = get_scores(act_a,act_b)

        score_a += sa
        score_b += sb

        if debug:
            print('╭── turn %02d ───╮'%(i_turn+1,))
            print('│ \x1b[91mA\x1b[39m: %2d \x1b[90m(%s\x1b[90m)\x1b[39m %s │'%(score_a,color_gain(sa),color_act(act_a)))
            print('│ \x1b[94mB\x1b[39m: %2d \x1b[90m(%s\x1b[90m)\x1b[39m %s │'%(score_b,color_gain(sb),color_act(act_b)))
            print('╰──────────────╯')

        actions_a.append(act_a)
        actions_b.append(act_b)

    return RoundResult(
        RoundResult.Player(actions_a,score_a),
        RoundResult.Player(actions_b,score_b)
    )
