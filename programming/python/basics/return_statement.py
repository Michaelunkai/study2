# # return statement = Function send Python values/objects back to the caller.
# # These values/objects are known as the function's return value

# def mulitiply(number1, number2):
#     result = number1 * number2
#     return result

# print(mulitiply(6,8))
# # output: 48


# i can also store the returned value whithin a variable:

# def mulitiply(number1, number2):
#     result = number1 * number2
#     return result

# x = mulitiply(6,8) 
# print(x)
# the output: 48

# this method use less amount of code:
def mulitiply(number1, number2):
    return number1 * number2
x = mulitiply(6,8) 
print(x)
# output: 48