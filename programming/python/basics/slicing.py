#Slicing = create a substring by extracting elements from another string
#          indexing[] or slice()
#          [start:stop:step]
# step is how much i increase my index by(between starting and stoping)

name = "Misha"

first_name = name[:3]
last_name = name[4:]
# funky_name = name[0:8:1]
funky_name = name[::2]
reversed_name = name[::-1]

# [0:8:1] will print my string. but [0:8:2] will print every second letter in my string etc
# [::2] start = 0. stop = end of string. step = 2
# reversed_name = name[::-1] - this will print my "name" variable backwards

# print(first_name)
#  print(last_name)
# print(funky_name)
# print(reversed_name)

# website1 = 'http://google.com'
# slice = slice(7,-4)

# print(website1[slice])
# this will print 'google' and remove 'http://' and '.com'
# website2 = 'http://wikipedia.com'
# slice = slice(7,-4)
# print(website2[slice])
# will also do same for every http website
website3 = 'https://wikipedia.com'
slice = slice(8,-4)
print(website3[slice])
#  slice(7,-4) - to slice http website. slice(8,-4) - to slice https website.