# #type casting = convert the data type of a value to another data type

# x = 1 #int
# y = 2.0 #float
# z = "3" #str

# print(x)
# print(int(y))
# print(z)

# ## print(y) = float. print(int(y)) = int

# x = 1 #int
# y = 2.0 #float
# z = "3" #str

# x = float(x)
# x = float(y)
# x = float(z)

# print(x)
# print(y)
# print(z*3)

#output:

#3.0
#2.0
#333

# x = 1 #int
# y = 2.0 #float
# z = "3" #str

# x = str(x)
# x = str(y)
# x = str(z)

# print(x)
# print(y)
# print(z*3)

##output:

#3
#2.0
#333

# x = 1 #int
# y = 2.0 #float
# z = "3" #str

# print("X is "+x)
# print("Y is "+y)
# print(z*3)

##output:
# Traceback (most recent call last):
#   File "d:\study\python\typecasting.py", line 53, in <module>
#     print("X is "+x)
#           ~~~~~~~^~
# TypeError: can only concatenate str (not "int") to str

###to fix the error, ill use type casting to convert int or float into a string:

x = 1 #int
y = 2.0 #float
z = "3" #str

print("X is "+str(x))
print("Y is "+str(y))
print(z*3)

##output:

# X is 1
# Y is 2.0
# 333

