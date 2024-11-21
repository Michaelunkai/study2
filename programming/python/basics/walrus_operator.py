# walrus operator :=
# assignment expression aka walrus operator
# assign values to variables as part of a larger expression

# foods = list()
# while True:
#     food = input("What food do youl like?: ")
#     if food == "quit":
#         break
#     foods.append(food)

# now the same, using walrus operator:

foods = list()
while food := input("what food do you like? : ") != "quit":
    foods.append(food)