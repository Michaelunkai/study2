# dictionary = a changeable, unordered collection of unique key:value pairs
#              fast because they use hashing, allow us to access a value quickly

# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}

# print(capitals['Russia'])
# the dictonary is 'capitals. this code will print 'Moscow'
# I Cant add keys as print function if they are not in the dictonary.

# to check if a key is availabe in the dictonary:
# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}

# print(capitals.get('Germany'))
# # the output: None

# method to print only the keys:
# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}
# only the keys, not the values:
# print(capitals.keys())
# output: dict_keys(['USA', 'India', 'china', 'Russia'])

# only the values, not the keys: 
# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}
# print(capitals.values())
# output: dict_values(['Washington DC', 'new dehli', 'beijing', 'Moscow'])

# both the keys & items:
# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}
# print(capitals.items())
# output: dict_items([('USA', 'Washington DC'), ('India', 'new dehli'), ('china', 'beijing'), ('Russia', 'Moscow')])

# dispaly all the key value pairs in a dictionary with 'for loop' :

# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}

# for key,value in capitals.items():
#     print(key, value)
# this will print my entire dictionary:
# USA Washington DC
# India new dehli
# china beijing
# Russia Moscow

# a feature of dictionaries: they are mutable. wich means i can change them after the program is already running.
# one way to do that: use the update method of dictionaries:

# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}

# capitals.update({'Germany':'Berlin'})

# for key,value in capitals.items():
#     print(key, value)
#  i can use the update method to add listing to directory, and also to change existing one:

# capitals = {'USA':'Washington DC',
#             'India': 'new dehli',
#             'china': 'beijing',
#             'Russia':'Moscow'}

# capitals.update({'Germany':'Berlin'})
# capitals.update({'Usa': 'Las Vegas'})

# for key,value in capitals.items():
#     print(key, value)

# output:
# USA Washington DC
# India new dehli
# china beijing
# Russia Moscow
# Germany Berlin
# Usa Las Vegas


# i can also reove a listing with the pop option:
# capitals.pop('China')

# i can also remove everything with 'clear':
# capitals.clear()

