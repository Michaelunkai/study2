# Lambda Functions and Higher-Order Functions

# Lambda Function
square = lambda x: x ** 2
print("Square of 5:", square(5)) # output: 25

# Higher-Order Function
def operate(func, num):
    return func(num)
#output: Square of 5: 25

# Using the higher-order function with the lambda function
result = operate(lambda x: x * 2,3)
print("Result of doubling 3:", result) #Output: 6