# Koopa

## Testing

By default, bot A and B use function `run` from `bot.py`

Basic usage:
```sh
python3 test.py
```

With arbitrary files/functions:
```sh
python3 test.py -a bot.py
python3 test.py -a run@bot.py
python3 test.py -a bot.py:run
python3 test.py -a-file bot.py -a-func run
```
