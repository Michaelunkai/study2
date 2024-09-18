# # zip function

# # The zip function in Python
# # combines corresponding elements from multiple 
# # iterables into tuples,
# # creating an iterator that produces pairs
# # of elements.

# # usernames = ["Dude", "Bro", "Mister"]
# # passwords = ("password","Abc", "guest")

# # to zip elements from each iterable togheter,so thair in pairs,
# #  and each pair is going to be stored as a tuple within a zip object:

# # users = zip(usernames, passwords)

# # for i in users:
# #     print(i)

# # output:
# # ('Dude', 'password')
# # ('Bro', 'Abc')
# # ('Mister', 'guest')
    
# # we got a zip object of tuples! and each tuple store each pair of elemts of my 2 itetables/



# # usernames = ["Dude", "Bro", "Mister"]
# # passwords = ("password","Abc", "guest")

# # users = list(zip(usernames, passwords))

# # for i in users:
# #     print(i)

# # output: 
# # ('Dude', 'password')
# # ('Bro', 'Abc')
# # ('Mister', 'guest')


# usernames = ["Dude", "Bro", "Mister"]
# passwords = ("password","Abc", "guest")

# users = dict(zip(usernames, passwords))

# for key,value in users.items():
#     print(key+" : "+value)

# # output:
# # Dude : password
# # Bro : Abc
# # Mister : guest

# ---------------------------------------------------

usernames = ["Dude", "Bro", "Mister"]
passwords = ("password","Abc", "guest")
login_date = ["1/1/2021","1/2/2021","1/3/2021"]

users = zip(usernames,passwords,login_date)

for i in users:
    print(i)

# output:
# ('Dude', 'password', '1/1/2021')
# ('Bro', 'Abc', '1/2/2021')
# ('Mister', 'guest', '1/3/2021')