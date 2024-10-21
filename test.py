#!/usr/bin/env python3

from pathlib import Path

from sys import argv

from sim import play_round, Bot

from itertools import combinations_with_replacement

default_bot_path = str(Path('bots/bot.py').absolute())
default_bot_func = 'run'

bot_a = Bot(default_bot_path,default_bot_func)
bot_b = Bot(default_bot_path,default_bot_func)

argv.pop(0)

test = 'single'

grid = []

def parse_botspec(spec: str) -> tuple[str,str]:
    func = None
    if '@' in spec:
        func, path = spec.split('@')
    elif ':' in spec:
        path, func = spec.split(':')
    else:
        path = spec
    func = func or 'run'
    path = path or 'bots/bots.py'
    return path, func

while len(argv):
    arg = argv.pop(0)
    for n, bot in ( ('a',bot_a), ('b',bot_b) ):
        if arg == '-'+n:
            bot.path, bot.func = parse_botspec(argv.pop(0))
        if arg == '-'+n+'-func':
            bot.func = argv.pop(0)
        if arg == '-'+n+'-path':
            bot.path = argv.pop(0)
    if arg == '-test':
        test = argv.pop(0)
        if test == 'grid':
            grid = argv.pop(0).split(',')

if test == 'single':
    
    play_round(bot_a, bot_b, debug=True)

elif test == 'long':
    
    sa = sb = 0
    wa = wb = 0
    
    for _ in range(100000):
        result = play_round(bot_a, bot_b)
        
        if not result:
            exit(1)
            
        sa += result.a.score
        sb += result.b.score
        
        wa += result.a.score > result.b.score
        wb += result.b.score > result.a.score
    
    wt = wa+wb
    print('A: %d (score %.2f%%) (wins %.2f%%)'%(sa,((sa-sb)/sa)*100,(wa/wt)*100))
    print('B: %d (score %.2f%%) (wins %.2f%%)'%(sb,((sb-sa)/sb)*100,(wb/wt)*100))

elif test == 'grid':
    g: dict[tuple[int,int],tuple[int,int]] = {}
    t: list[int] = [0 for _ in range(len(grid))]
    
    for i, (ia, ib) in enumerate(combinations_with_replacement(range(len(grid)),2)):
        a,b = grid[ia],grid[ib]
        sa = sb = 0
        
        for _ in range(1000):
            result = play_round(
                Bot(*parse_botspec(a)),
                Bot(*parse_botspec(b))
            )
            if not result:
                exit(1)
            
            sa += result.a.score
            sb += result.b.score
            t[ia] += result.a.score
            t[ib] += result.b.score
        
        g[(ia,ib)] = (sa,sb)
        
    for k, (i, s) in enumerate(sorted(enumerate(t),key=lambda u:u[1],reverse=True)):
        path, func = parse_botspec(grid[i])
        print('%2d \x1b[95m%s\x1b[90m:%s\x1b[39m : %d'%(k+1,path,func,s))
    
    # for (ia, ib), s in g.items():
    #     a,b = grid[ia],grid[ib]
    #     sa,sb = s
    #     path_a,func_a = parse_botspec(a)
    #     path_b,func_b = parse_botspec(b)
    #     rows_a,rows_b = [],[]
    #     print('─── \x1b[95m%s\x1b[90m:\x1b[95m%s\x1b[39m \x1b[90m(\x1b[91;%dmA\x1b[22;90m)\x1b[39m vs \x1b[95m%s\x1b[90m:\x1b[95m%s\x1b[39m \x1b[90m(\x1b[94;%dmB\x1b[22;90m)\x1b[39m ───'%(path_a,func_a,1 if sa>sb else 2,path_b,func_b,1 if sb>sa else 2))
    #     for i, (rows,j) in enumerate((
    #         (rows_a,ia),
    #         (rows_b,ib)
    #     )):
    #         p,q = s[::1-2*i]
    #         r = (p-q)/(max(p,q) or 1)
    #         # rows.extend((
    #         #     ('score',  str(p), None),
    #         #     ('score%', '%.2f'%(r,), )
    #         # ))

else:
    print('Bad test kind %s'%(repr(test),))
    exit(1)
