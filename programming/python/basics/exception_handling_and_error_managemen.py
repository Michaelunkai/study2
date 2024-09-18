#  exception handling and error management 

# Basic try-except block
try:
    results = 10 / 0 
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Handling multiple exceptions
try:
    num = int(input('Enter number: '))
    result = 10 / num
    print('Result:', result)
except ZeroDivisionError:
    print('Cannot divide by zero!')
except ValueError:
    print('Invalid input. Please enter a number')
else:
    print('No exeptions occurred')

# finally block
try:
    file: open('nonexistent_file.txt', 'r')
except FileExistsError:
    print('File not found!')
finally:
    print('This block will always run, regardless of exeptions.')
    