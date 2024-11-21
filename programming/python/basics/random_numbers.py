# # random numbers

# import random
# x = random.randint(1,6)
# print(x)
# # output: 6


# import random
# y = random.random()
# x = random.randint(1,6)
# print(y)
# output: a random floating number between 0 and 1.

# import random
# x = random.randint(1,6)
# y = random.random()
# myList = ['rock', 'paper', 'scissors']
# z = random.choice(myList)
# print(z)
# output: will randomly print one of the items in myList list

import random
x = random.randint(1,6)
y = random.random()
myList = ['rock', 'paper', 'scissors']
z = random.choice(myList)
cards = [1,2,3,4,5,6,7,8,9,"J","Q","K","A"]
random.shuffle(cards)
print(cards)
#  will randomly shuffle the items inside 'cards'