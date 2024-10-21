#!/usr/bin/env python3

from pathlib import Path

from sys import argv

from sim import play_round, Bot

default_bot_path = str(Path('bot.py').absolute())
default_bot_func = 'run'

bot_a = Bot(default_bot_path,default_bot_func)
bot_b = Bot(default_bot_path,default_bot_func)

argv.pop(0)

while len(argv):
    arg = argv.pop(0)
    for n, bot in ( ('a',bot_a), ('b',bot_b) ):
        if arg == '-'+n:
            spec = argv.pop(0)
            if '@' in spec:
                bot.func, bot.path = spec.split('@')
            elif ':' in spec:
                bot.path, bot.func = spec.split(':')
            else:
                bot.func = 'run'
                bot.path = spec
        if arg == '-'+n+'-func':
            bot.func = argv.pop(0)
        if arg == '-'+n+'-path':
            bot.path = argv.pop(0)

play_round(bot_a, bot_a, debug=True)
