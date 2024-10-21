#!/usr/bin/env python3

from pathlib import Path

from sim import play_round, Bot

bot_path = str(Path('bot.py').absolute())
bot_func = 'run'

bot = Bot(bot_path,bot_func)

play_round(bot, bot, True)
