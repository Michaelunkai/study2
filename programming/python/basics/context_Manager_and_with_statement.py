# context Manager and with statement
# Context Manager for file handling

with open("example.txt", "w") as file:
    file.write("This is an example file.")

# Reading from the file using the with statement
with open("example.txt", "r") as file:
    content = file.read()
    print("File content:", content)

# output: File content: This is an example fil
    
# In this step, we're introducing context managers and the with statement. Context managers help manage resources, such as file handling, in a clean and efficient way. The with statement ensures
# that resources are properly acquired and released, even if an exception occurs. 