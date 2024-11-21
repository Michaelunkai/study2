#  if statement = a block of code that will execute if it's condition is true

# age = int(input("How old are you?: "))

# if age >= 18:
#     print("You are an adult!")
# elif age == 100:
#     print("You old, man!")
# # to check if variable = integer, use == not =.
# elif age < 10:
#     print("You are a baby!")
# else:
#     print("You are a kid!")

# this will print the 'if age' statemnent if ill input 100, because the order is imoortant. this is how to do it proparly:

age = int(input("How old are you?: "))

if age == 100:
    print("You old, man!")
elif age >= 18:
    print("You are an adult!")
# to check if variable = integer, use == not =.
elif age < 10:
    print("You are a baby!")
else:
    print("You are a kid!")
