from itertools import product

def generate_all_strategies(turns):
    actions = ["cooperate", "nothing", "cheat"]
    # Generate combinations for two players
    return product(actions, repeat=turns * 2)

def main():
    out=""
    turns = 10
    strategies = generate_all_strategies(turns)

    
    # Print strategies
    for index, strategy in enumerate(strategies):
        player1_actions = strategy[:turns]
        player2_actions = strategy[turns:]
        out+=f"Strategy {index + 1}; Player 1: {player1_actions}, Player 2: {player2_actions}\n"
    return out

if __name__ == "__main__":
    with open("info.txt", "w")as file: file.write(main())


# This would take 40 days to run.