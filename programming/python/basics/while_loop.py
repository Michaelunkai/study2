# # # while loop = a statement that will execute it's block of code, 
# # #              as long as it's condition remains true

# # # infinite loop:
# # while 1==1:
# #     print('help! im in a loop!')
# # # top prompt a user to type in their' name and escape the infinte while loop:
# name = ''

# while len(name) == 0:
#     name = input('Enter your name: ')

# print('Hello '+name)

# another way: 
name = None

while not name:
    name = input("Enter your name: ")

print("Hello "+name)

# conclusion: a while loop is a statement that will execute a block of code as long as itss condition stay's true.