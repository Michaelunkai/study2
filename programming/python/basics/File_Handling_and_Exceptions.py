# File Handling and Exceptions
# File Handling - Writing to a file
with open('sample.txt', 'w') as file:
    file.write('Hello, this is a sample file')

# Reading from the file
with open('sample.txt', 'r') as file:
    content = file.read()
    print('File content:', content)

# Exceptions
try:
    num = int(input('Enter a number: '))
    result = 10 / num
    print('Result:', result)
except ZeroDivisionError:
    print('Cannot divide by zero!')
except ValueError:
    print('Invalid input. Please enter a number.')

# output:
#     PS C:\Users\micha> & C:/Users/micha/AppData/Local/Microsoft/WindowsApps/python3.12.exe "c:/study/python/File Handling and Exceptions.py"
# File content: Hello, this is a sample file
# Enter a number: 2
# Result: 5.0
# PS C:\Users\micha> & C:/Users/micha/AppData/Local/Microsoft/WindowsApps/python3.12.exe "c:/study/python/File Handling and Exceptions.py"
# File content: Hello, this is a sample file
# Enter a number: 1
# Result: 10.0