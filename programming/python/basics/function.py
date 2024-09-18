# # function = a block of code which is executed only when it is called.

# def hello(first_name,last_name,age):
#     print('hello '+first_name+' '+last_name)
#     print('you are '+str(age)+' years old')
#     print('have a nice day!!')

# hello('misha','fedro',21)
# # output:
# # hello misha fedro
# # you are 21 years old
# # have a nice day!!

# def hello():
#     print('hello!')

# hello()
# hello()
# hello()

# output:
# hello!
# hello!
# hello!

# def hello():
#     print('hello!')
#     print('have a nice day!')
# hello()
# hello()
# hello()

# output:
# hello!
# have a nice day!
# hello!
# have a nice day!
# hello!
# have a nice day!


# def hello(name):
#     print('hello! '+name)
#     print('have a nice day!')

# hello('misha')
# sending info to a function, called = 'arguments'
# when defining the function, i need a matching set of 
#  paramenters


# def hello(first_name,last_name):
#     print('hello! '+first_name+' '+last_name)
#     print('have a nice day!')

# hello('misha', 'fedro')

# # output:
# hello! misha fedro
# have a nice day!

# with arguments, i can mix and mtch the data types that im sending 
# as arguments. in the code above, im sending 2 string values as arguments. 

# this time ill send an int value:

def hello(first_name,last_name,age):
    print('hello! '+first_name+' '+last_name)
# if i need to display an int or number along with string, i need to 
# convert it to a string:
    print('You are '+str(age)+' years old'+last_name)
    print('have a nice day!')

hello('misha', 'fedro',28)

# # output:
# hello! misha fedro
# You are 28 years oldfedro
# have a nice day!

#  a fuction is a block of code which executed only when its called!