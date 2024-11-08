#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from itertools import combinations_with_replacement
from glob import glob
from math import copysign

from sim import play_round, Bot

default_bot_path = str(Path('bots/rand.py').absolute())
default_bot_func = 'run'

bot_a = Bot(default_bot_path,default_bot_func)
bot_b = Bot(default_bot_path,default_bot_func)

argv.pop(0)

test = 'single'

grid = []

def specialized_color_gain(n: float) -> str:
    if n == 0:
        return '   \x1b[33m0.00\x1b[39m'
    c = '32' if n > 0 else '31'
    # return '\x1b[%sm%s'%(c,str(round(abs(n),2)).rjust(6, ' ')) # What am I doing seriously..
    return '\x1b[%sm%7.2f'%(c,n)

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
            w = argv.pop(0)
            if w == '*':
                grid = glob('bots/*.py')
            else:
                grid = w.split(',')

if test == 'single':
    
    play_round(bot_a, bot_b, debug=True)

elif test == 'long':
    
    # We wanna understand ! So here are the abreviation :>
    # sa  = score a
    # sb  = score b
    # wa  = win a
    # wb  = win b
    # wt  = win total
    # pf1 = percentage false 1
    # pf2 = percentage false 2
    # pt1 = percentage true 1
    # pt2 = percentage true 1

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

    # Yeah don't check 'specialized_color_gain', your eyes wont survive.
    m = "%\x1b[39m"
    pf1 = specialized_color_gain(((sa-sb)/(sa or 1))*100)+m
    pf2 = specialized_color_gain(((sb-sa)/(sb or 1))*100)+m
    pt1 = '%6.2f'%((wa/(wt or 1))*100,) # Doing some weird stuff to add space before numbers, so it takes the same place no matter what.
    pt2 = '%6.2f'%((wb/(wt or 1))*100,)
    
    print('╭──── \x1b[38;5;146mresults\x1b[39m ───────────────────╮')
    print(f'│ \x1b[91mA\x1b[39m: {sa:< 8} \x1b[90m({pf1}\x1b[90m)\x1b[39m {pt1}% │') # Man I prefer format, pls.
    print(f'│ \x1b[94mB\x1b[39m: {sb:< 8} \x1b[90m({pf2}\x1b[90m)\x1b[39m {pt2}% │')
    print('╰────────────────────────────────╯')
    # print('A: %d (score %.2f%%) (wins %.2f%%)'%(sa,((sa-sb)/sa)*100,(wa/wt)*100))
    # print('B: %d (score %.2f%%) (wins %.2f%%)'%(sb,((sb-sa)/sb)*100,(wb/wt)*100))

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
    
    print('┄─ \x1b[38;5;185mLeaderboard\x1b[39m ─┄')
    
    ms = max(t)
    ls = min(t)
    for k, (i, s) in enumerate(sorted(enumerate(t),key=lambda u:u[1],reverse=True)):
        path, func = parse_botspec(grid[i])
        t = (s-ls)/(ms-ls)*100 # or (s/ms)*100
        print('%2d %3d \x1b[95m%s\x1b[90m:%s\x1b[39m : %d'%(k+1,t,path,func,s))
        
    print('\n┄─ \x1b[38;5;185mDetailed comparison\x1b[39m ─┄')
    
    for (ia, ib), s in g.items():
        a,b = grid[ia],grid[ib]
        sa,sb = s
        path_a,func_a = parse_botspec(a)
        path_b,func_b = parse_botspec(b)
        rows_a,rows_b = [],[]
        # print('─── \x1b[95m%s\x1b[90m:\x1b[95m%s\x1b[39m \x1b[90m(\x1b[91;%dmA\x1b[22;90m)\x1b[39m vs \x1b[95m%s\x1b[90m:\x1b[95m%s\x1b[39m \x1b[90m(\x1b[94;%dmB\x1b[22;90m)\x1b[39m ───'%(path_a,func_a,1 if sa>sb else 2,path_b,func_b,1 if sb>sa else 2))
        for i, (rows,j) in enumerate((
            (rows_a,ia),
            (rows_b,ib)
        )):
            # Score percentage could be reworked
            p,q = s[::1-2*i]
            r = p/(max(p,q) or 1)
            rows.extend((
                ('score',  str(p)),
                # Not sure which one is best
                # ('score%', '%.2f'%(r*100,), '91' if r < 1 else '92')
                ('', '%.2f%%'%(r*100,), '\x1b['+('91;2' if p < q else '92;1')+'m', '\x1b[39;22m')
            ))
        colsize_a_h = len(path_a)+len(func_b)+3
        colsize_a_l = max(map(lambda r:len(r[0]),rows_a))
        colsize_a_r = max(map(lambda r:len(r[1]),rows_a))
        colsize_a_t = max(colsize_a_h,colsize_a_l+colsize_a_r+1)
        colsize_a_r += max(0,colsize_a_t-colsize_a_r-colsize_a_l-1)
        colsize_b_h = len(path_b)+len(func_b)+3
        colsize_b_l = max(map(lambda r:len(r[0]),rows_b))
        colsize_b_r = max(map(lambda r:len(r[1]),rows_b))
        colsize_b_t = max(colsize_b_h,colsize_b_l+colsize_b_r+1)
        colsize_b_r += max(0,colsize_b_t-colsize_b_r-colsize_b_l-1)
        print('╭'+('{:─^%ds}'%(colsize_a_t+16)).format(' \x1b[38;5;146m'+path_a+':'+func_a+'\x1b[39m ')+'╮ ╭'+('{:─^%ds}'%(colsize_b_t+16)).format(' \x1b[38;5;146m'+path_b+':'+func_b+'\x1b[39m ')+'╮')
        for ra, rb in zip(rows_a,rows_b):
            sa,sb = (ra[2] if len(ra) > 2 and ra[2] else ''),(rb[2] if len(rb) > 2 and rb[2] else '')
            ta,tb = (ra[3] if len(ra) > 3 and ra[3] else ''),(rb[3] if len(rb) > 3 and rb[3] else '')
            print('│'+('{:<%d} {:>%d}\x1b[39m'%(colsize_a_l,colsize_a_r+len(sa+ta))).format(ra[0],sa+ra[1]+ta)+'│ │'+('{:<%d} {:>%d}'%(colsize_b_l,colsize_b_r+len(sb+tb))).format(rb[0],sb+rb[1]+tb)+'│')
        print('╰'+'─'*colsize_a_t+'╯ ╰'+'─'*colsize_b_t+'╯')

else:
    print('Bad test kind %s'%(repr(test),))
    exit(1)
