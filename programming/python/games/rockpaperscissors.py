import random

while True:
    choices = ["rock", "paper", "scissors"]

    computer = random.choice(choices)
    player = None

    while player not in choices:    
        player = input("rock, paper, or scissors?: ").lower()

    if player == computer:
        print("computer: ",computer)
        print("player: ",player)
        print("Tie!")
    elif player == "rock":
        if computer == "paper":
            print("computer: ",computer)
            print("player: ",player)
            print("you lose!")
        if computer == "scissors":
            print("computer: ",computer)
            print("player: ",player)
            print("you Win!")
    elif player == "scissors":
        if computer == "rock":
            print("computer: ",computer)
            print("player: ",player)
            print("you lose!")
        if computer == "paper":
            print("computer: ",computer)
            print("player: ",player)
            print("you Win!")
    elif player == "paper":
        if computer == "scissors":
            print("computer: ",computer)
            print("player: ",player)
            print("you lose!")
        if computer == "rock":
            print("computer: ",computer)
            print("player: ",player)
            print("you Win!")

    play_again = input("Play again? (yes/no): ").lower()
# != - not equal
    if play_again != "yes":
        break
print("bye!!")