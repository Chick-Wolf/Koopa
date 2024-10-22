# Koopa

## Testing

By default, bot A and B use function `run` from `bots/rand.py`

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

To run many games against bots A and B:
```sh
python3 test.py -test long
```

To run several bots against themselves:
```sh
python3 test.py -test grid bots/rand.py,bots/troll.py,bots/nothing.py
python3 test.py -test grid '*' # For all of them
```
