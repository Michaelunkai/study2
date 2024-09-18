# keyboard arguments =          arguments preceded by an identifier when we pass them to a function
                                # the order of the arguments dosn't matter, unlike positional arguments
                                # python knows the names of the arguments that our function recives

def hello(first,middle,last):
    print('Hello '+first+' '+middle+' '+last)


hello(last='Fedro',middle='King',first='Misha')
# output:
# Hello Misha King Fedro

