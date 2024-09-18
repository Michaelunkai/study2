#  rock, papar, scissors

# import random
# choices = ["rock", "paper", "scissors"]
# computer = random.choice(choices)
# print(computer)
# outout: wil randomly print one of the options inside "choices"

# import random
# choices = ["rock", "paper", "scissors"]
# computer = random.choice(choices)
# player = input("rock, paper, or scissors?: ")
# print(computer)
# print(player)
# output:
# rock, paper, or scissors?: rock
# paper
# rock

# import random
# choices = ["rock", "paper", "scissors"]
# computer = random.choice(choices)
# player = input("rock, paper, or scissors?: ")
# print("computer: ",computer)
# print("player: ",player)

# output: 
# rock, paper, or scissors?: paper
# computer:  scissors
# player:  paper


# import random
# choices = ["rock", "paper", "scissors"]

# computer = random.choice(choices)
# player = None

# while player not in choices:    
#     player = input("rock, paper, or scissors?: ")
# print("computer: ",computer)
# print("player: ",player)
# this wll limit the output options only to rock, paper and scissors.

# import random
# choices = ["rock", "paper", "scissors"]

# computer = random.choice(choices)
# player = None

# while player not in choices:    
#     player = input("rock, paper, or scissors?: ").lower()

# print("computer: ",computer)
# print("player: ",player)
# will allow to use apper cases and will read it in output sd lower

# import random
# choices = ["rock", "paper", "scissors"]

# computer = random.choice(choices)
# player = None

# while player not in choices:    
#     player = input("rock, paper, or scissors?: ").lower()

# if player == computer:
#     print("computer: ",computer)
#     print("player: ",player)
#     print("Tie!")
# elif player == "rock":
#     if computer == "paper":
#         print("computer: ",computer)
#         print("player: ",player)
#         print("you lose!")
#     if computer == "scissors":
#         print("computer: ",computer)
#         print("player: ",player)
#         print("you Win!")
# elif player == "scissors":
#     if computer == "rock":
#         print("computer: ",computer)
#         print("player: ",player)
#         print("you lose!")
#     if computer == "paper":
#         print("computer: ",computer)
#         print("player: ",player)
#         print("you Win!")
# elif player == "paper":
#     if computer == "scissors":
#             print("computer: ",computer)
#             print("player: ",player)
#             print("you lose!")
#     if computer == "rock":
#             print("computer: ",computer)
#             print("player: ",player)
#             print("you Win!")

# output:
# rock, paper, or scissors?: paper
# computer:  scissors
# player:  paper
# you lose!


# add feature that ask yhe player for another round:

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