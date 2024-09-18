# *args = parameter that will pack all arguments into a tuple
# useful so that a function can accept a varying amount of arguments

# Arguments passed to a function or script for customization and execution.


# def add(*stuff):
#     sum = 0
#     stuff = list(stuff)
#     stuff[0] = 0
#     for i in stuff:
#         sum += i
#     return sum

# print(add(1,2,3,4,5,6))

# def add(num1,num2):
#     sum = num1 + num2
#     return sum
# print(add(1,2))

# output: 3 
# def add(num1,num2):
#     sum = num1 + num2
#     return sum
# print(add(1,2))

# if i had 3 numbers as arguments instead of 2(1,2,3)
# i could not longer use this set of functions, bacause
# i have only 2 parementers set up(num1,num2). so i need to fix it:

# def add(num1,num2,num3):
#     sum = num1 + num2 + num3
#     return sum
# print(add(1,2,3))
# output: 6

# def add(*args):
#     sum = 0
#     for i in args:
#         sum += i 
#         return sum
# print(add(1,2,3))
# output: 1 

# def add(*args):
#     sum = 0
#     for i in args:
#         sum += i 
#         return sum
# print(add(1,2,3,4,5,6))

# def add(*stuff):
#     sum = 0
#     stuff = list(stuff)
#     for i in stuff:
#         sum += i 
#     return sum
# print(add(1,2,3,4,5,6))
# output: 21

def add(*stuff):
    sum = 0
    stuff = list(stuff)
    stuff[0] = 0
    for i in stuff:
        sum += i 
    return sum
print(add(1,2,3,4,5,6))
# output:20