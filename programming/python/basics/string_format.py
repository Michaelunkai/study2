# string format
# str.format() =    optional method that gives users
        # more control  when displaying output

# animal = 'cow'
# item = 'moon'

# print('The '+animal+' jumped over the '+item)
# output: The cow jumped over the moon

# more alegant way, using the format method available to strings.

# animal = 'cow'
# item = 'moon'

# print('The {} jumped over the {}'.format('cow','moon'))
# output: The cow jumped over the moon

# animal = 'cow'
# item = 'moon'

# print('The {} jumped over the {}'.format(animal,item)) #positional argument
# print('The {0} jumped over the {1}'.format(animal,item))
# print('The {animal} jumped over the {item}'.format(animal='cow',item='moon')) #keyboard argument
# output:The cow jumped over the moon

# animal = 'cow'
# item = 'moon' 
# text = 'The {} jumped over the {}'
# print(text.format(animal,item))

#  add some padding to a string when i display it,
#  using the format method:

# name ='Misha'
# print('Hello, my name is {}'.format(name))
# output: Hello, my name is Misha

# name ='Misha'
# print('Hello, my name is {:10}. nice to meet you'.format(name))
# output: Hello, my name is Misha     . nice to meet you
# print('Hello, my name is {:>10}. nice to meet you'.format(name))
# output: Hello, my name is      Misha. nice to meet you

# print('Hello, my name is {:^10}. nice to meet you'.format(name))
# output: Hello, my name is   Misha   . nice to meet you

# lets format some numbers:
# number = 3.14159
# to display only the 2 numbers after the '.' : 
# print('The number pi is {:.2f}'.format(number))
# f - floating point numbers
# output: The number pi is 3.14

number = 1000
# print('The number pi is {:,}'.format(number))
# output: The number pi is 1,000

# to get binary representation of my number:
# print('The number pi is {:b}'.format(number))
# output: The number pi is 1111101000

# octal number:
# print('The number pi is {:o}'.format(number))
# output: The number pi is 1750

# hexadecimal:
# print('The number pi is {:x}'.format(number))
# output: The number pi is 3e8

# scientfic notation:
print('The number pi is {:e}'.format(number))
# output: The number pi is 1.000000e+03