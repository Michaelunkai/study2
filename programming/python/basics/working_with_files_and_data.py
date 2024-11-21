# Writing to a file
with open('example.txt', 'w') as file:
    file.write('Hello, this is an example file.')

# Reading from a file
with open('example.txt', 'r') as file:
    content = file.read()
    print('File Content:', content)

# Data manipulation with lists
numbers = [1, 2, 3, 4, 5]

# Filtering even numbers
even_numbers = [num for num in numbers if num % 2 == 0]
print('Even Numbers:', even_numbers)

# Mapping to squares
squared_numbers = list(map(lambda x: x**2, numbers))
print('Squared Numbers:', squared_numbers)

# Reducing to the sum
from functools import reduce
sum_of_numbers = reduce(lambda x, y: x + y, numbers)
print('Sum of Numbers:', sum_of_numbers)


# # output: 
# File Content: Hello, this is an example file.
# Even Numbers: [2, 4]
# Squared Numbers: [1, 4, 9, 16, 25]
# Sum of Numbers: 15
