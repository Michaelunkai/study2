#input("what is your name?: ")
#assign variable:
# name = input("what is your name?: ")
# age = input("How old are you?: ")

# age = age + 1

# print("Hello " + name)

#the output for this:
# name = input("what is your name?: ")
# age = input("How old are you?: ")

# age = age + 1

# print("Hello " + name)

# is this:
#what is your name?: sha
#How old are you?: 12
#Traceback (most recent call last):
#  File "/mnt/d/userinput.py", line 6, in <module>
#    age = age + 1
#TypeError: can only concatenate str (not "int") to str
#>>>


#the fix:

name = input("what is your name?: ")
age = int(input("How old are you?: "))
height = float(input("How tall are you?: "))


print("Hello " +name)
print("You are "+str(age)+" years old")
print("You are "+str(height) +"cm tall")