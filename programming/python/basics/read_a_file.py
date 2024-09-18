# read a file 
# with open('C:\\Users\\micha\\Downloads\\a.txt') as file:
#     print(file.read())
# this will print the text inside my file
    
# with open('C:\\Users\\micha\\Downloads\\a.txt') as file:
#     print(file.read())
# print(file.closed)
# output:
# try
# True

try:
    with open('C:\\Users\\micha\\Downloads\\a.tx') as file:
        print(file.read())
except FileNotFoundError:
    print("That file was not found!")

# output: That file was not found!