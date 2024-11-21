# variable scope
# scope =       the region that a variable os recognized
#               a variable is only available from  inside the region it is created.
#               a global and locally scoped versions of a variable can be created

# def display_name():
#     name = 'Misha' # local scope (available only inside this function)
#     print(name)
# this variable have a local scope, because
# its declaired inside of s function.

# on the other hand, global variable is a variable declared outside of any function,
# than the modul that im working with.


# name = 'Misha' # global scope (availabe only inside this function)
# def display_name():
#     name = 'Misha'  # local scope (available only inside this function)
#     print(name)

# print(name)
# output: Misha

# name = 'Misha' # global scope (availabe only inside this function)
# def display_name():
#     name = 'Misha'  # local scope (available only inside this function)
#     print(name)

# display_name()
# print(name)
# output:

# Misha
# Misha

name = 'Misha' # global scope (availabe only inside this function)
def display_name():
    print(name)

display_name()
print(name)