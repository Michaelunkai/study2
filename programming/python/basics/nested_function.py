# # nested function calls = function calls inside other function calls
# #                         innermost function calls are resolved first
# #                         return value is used as argument for the next outer function

# num = input('Enter a whole positive number: ')
# num = float(num)
# num = abs(num)
# num = round(num)
# print(num)
# # output:
# Enter a whole positive number: 2
# 2

# here a way to achive the same with one line of code:
print(round(abs(float(input('Enter a whole positive number: ')))))

