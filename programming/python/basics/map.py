# map
# applies a function ti each item in an iterable (list, tuple, etc)

# map(function, iterable)

# store = [("shirts",20.00),
#          ("pants",25.00),
#          ("jacket",50.00),
#          ("socks",10.00)]

# to_euros = lambda data: (data[0],data[1]*0.82)

# store_euros = list(map(to_euros, store))

# for i in store_euros:
#     print(i)
# output:
# ('shirts', 16.4)
# ('pants', 20.5)
# ('jacket', 41.0)
# ('socks', 8.2)
    
# convert from euros to usd:
    
store = [("shirts",20.00),
         ("pants",25.00),
         ("jacket",50.00),
         ("socks",10.00)]

to_euros = lambda data: (data[0],data[1]*0.82)
to_dollars =  lambda data: (data[0],data[1]/0.82)


store_dollars = list(map(to_euros, store))

for i in store_dollars:
    print(i)

# output:
# ('shirts', 16.4)
# ('pants', 20.5)
# ('jacket', 41.0)
# ('socks', 8.2)