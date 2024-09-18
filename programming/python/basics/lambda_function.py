# lambda function
# function written in 1 line using lambda keyword
# accepts any number of arguments, but only has one expression. (like a shortcut)
# useful if needed for a short period of time, throw-away)

# syntax:
#  lamnda parameters: expression
# def double(x):
#     return x * 2

# print(double(5))
# output : 10

double = lambda x:x * 2
multiply = lambda x, y: x * y
add = lambda x, y, z: x + y + z
full_name = lambda first_name, last_name: first_name+" "+last_name
age_check = lambda age:True if age >= 18 else False
print(age_check(12))
# output: False