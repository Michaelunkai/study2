# # quiz game
# #------------------------------
# def new_game():
#     pass
# #------------------------------
# def check_answer():
#     pass
# #------------------------------
# def display_score():
#     pass
# #------------------------------
# def play_again():
#     pass
# #------------------------------

# questions = {
#     "who create Python?: ": "A",
#     "What year was Python created?: ": "B",
#     "Python is tributed to which comedy group?: ": "C",
#     "Is the Earth round?: ": "A"
# }

# options = [["A. Guido van Rossum", "B. Elon Musk", "C. Bill Gates", "D. mark Zockerburg"],
#           ["A. 1989", "B. 1991", "C. 2000", "D. 2016"],
#           ["A. lonley Island", "B. Smosh", "C. Monty Python", "D. SNL"],
#           ["A. True", "B. False", "C. sometimes", "D. what's Earth?"]]

# new_game()

# quiz game
# #------------------------------
# def new_game():
    
#     guesses = []
#     correct_guesses = 0
#     question_num = 1

#     for key in questions:
#         print(key)
# #------------------------------
# def check_answer():
#     pass
# #------------------------------
# def display_score():
#     pass
# #------------------------------
# def play_again():
#     pass
# #------------------------------

# questions = {
#     "who create Python?: ": "A",
#     "What year was Python created?: ": "B",
#     "Python is tributed to which comedy group?: ": "C",
#     "Is the Earth round?: ": "A"
# }

# options = [["A. Guido van Rossum", "B. Elon Musk", "C. Bill Gates", "D. mark Zockerburg"],
#           ["A. 1989", "B. 1991", "C. 2000", "D. 2016"],
#           ["A. lonley Island", "B. Smosh", "C. Monty Python", "D. SNL"],
#           ["A. True", "B. False", "C. sometimes", "D. what's Earth?"]]

# new_game()

# output: who create Python?: 
# What year was Python created?: 
# Python is tributed to which comedy group?: 
# Is the Earth round?: 


# #------------------------------
# def new_game():
    
#     guesses = []
#     correct_guesses = 0
#     question_num = 1

#     for key in questions:
#         print("-------------------------")
#         print(key)
#         for i in options:
#             print(i)
# #------------------------------
# def check_answer():
#     pass
# #------------------------------
# def display_score():
#     pass
# #------------------------------
# def play_again():
#     pass
# #------------------------------

# questions = {
#     "who create Python?: ": "A",
#     "What year was Python created?: ": "B",
#     "Python is tributed to which comedy group?: ": "C",
#     "Is the Earth round?: ": "A"
# }

# options = [["A. Guido van Rossum", "B. Elon Musk", "C. Bill Gates", "D. mark Zockerburg"],
#           ["A. 1989", "B. 1991", "C. 2000", "D. 2016"],
#           ["A. lonley Island", "B. Smosh", "C. Monty Python", "D. SNL"],
#           ["A. True", "B. False", "C. sometimes", "D. what's Earth?"]]

# new_game()


# output:
# -------------------------
# who create Python?: 
# ['A. Guido van Rossum', 'B. Elon Musk', 'C. Bill Gates', 'D. mark Zockerburg']
# ['A. 1989', 'B. 1991', 'C. 2000', 'D. 2016']
# ['A. lonley Island', 'B. Smosh', 'C. Monty Python', 'D. SNL']
# ['A. True', 'B. False', 'C. sometimes', "D. what's Earth?"]
# -------------------------
# What year was Python created?: 
# ['A. Guido van Rossum', 'B. Elon Musk', 'C. Bill Gates', 'D. mark Zockerburg']
# ['A. 1989', 'B. 1991', 'C. 2000', 'D. 2016']
# ['A. lonley Island', 'B. Smosh', 'C. Monty Python', 'D. SNL']
# ['A. True', 'B. False', 'C. sometimes', "D. what's Earth?"]
# -------------------------
# Python is tributed to which comedy group?: 
# ['A. Guido van Rossum', 'B. Elon Musk', 'C. Bill Gates', 'D. mark Zockerburg']
# ['A. 1989', 'B. 1991', 'C. 2000', 'D. 2016']
# ['A. lonley Island', 'B. Smosh', 'C. Monty Python', 'D. SNL']
# ['A. True', 'B. False', 'C. sometimes', "D. what's Earth?"]
# -------------------------
# Is the Earth round?: 
# ['A. Guido van Rossum', 'B. Elon Musk', 'C. Bill Gates', 'D. mark Zockerburg']
# ['A. 1989', 'B. 1991', 'C. 2000', 'D. 2016']
# ['A. lonley Island', 'B. Smosh', 'C. Monty Python', 'D. SNL']
# ['A. True', 'B. False', 'C. sometimes', "D. what's Earth?"]

#------------------------------
def new_game():
    
    guesses = []
    correct_guesses = 0
    question_num = 1

    for key in questions:
        print("-------------------------")
        print(key)
        for i in options[question_num-1]:
            print(i)
        guess = input("Enter (A, B, C, or D): ")
        guess = guess.upper()
        guesses.append(guess)

        correct_guesses += check_answer(questions.get(key),guess)
        question_num += 1

    display_score(correct_guesses, guesses)

#------------------------------
def check_answer(answer, guess):
    
    if answer == guess:
        print("CORRECT!")
        return 1
    else:
        print("WRONG!")
        return 0
#------------------------------
def display_score(correct_guesses, guesses):
    print("---------------------------------")
    print("RESULTS")
    print("---------------------------------")

    print("Answers: ", end="")
    for i in questions:
        print(questions.get(i), end="")

    print("Guesses: ", end="")
    for i in guesses:
        print(i, end=" ")
    print()

    score = int((correct_guesses/len(questions))*100)
    print("Your score is: "+str(score)+"%")
#------------------------------
def play_again():
    
    response = input("Do you want to play again?: (yes or no): ")
    response = response.upper()

    if response == "YES":
        return True
    else:
        return False
#------------------------------

questions = {
    "who create Python?: ": "A",
    "What year was Python created?: ": "B",
    "Python is tributed to which comedy group?: ": "C",
    "Is the Earth round?: ": "A"
}

options = [["A. Guido van Rossum", "B. Elon Musk", "C. Bill Gates", "D. mark Zockerburg"],
          ["A. 1989", "B. 1991", "C. 2000", "D. 2016"],
          ["A. lonley Island", "B. Smosh", "C. Monty Python", "D. SNL"],
          ["A. True", "B. False", "C. sometimes", "D. what's Earth?"]]

new_game()

while play_again():
    new_game()

print("BYEEEE!!")

# output:

# who create Python?: 
# A. Guido van Rossum
# B. Elon Musk
# C. Bill Gates
# D. mark Zockerburg
# Enter (A, B, C, or D): a
# CORRECT!
# -------------------------
# What year was Python created?: 
# A. 1989
# B. 1991
# C. 2000
# D. 2016
# Enter (A, B, C, or D): b
# CORRECT!
# -------------------------
# Python is tributed to which comedy group?: 
# A. lonley Island
# B. Smosh
# C. Monty Python
# D. SNL
# Enter (A, B, C, or D): c
# CORRECT!
# -------------------------
# Is the Earth round?: 
# A. True
# B. False
# C. sometimes
# D. what's Earth?
# Enter (A, B, C, or D): a
# CORRECT!
# ---------------------------------
# RESULTS
# ---------------------------------
# Answers: ABCAGuesses: A B C A 
# Your score is: 100%
# do you want to play again? (yes or no)