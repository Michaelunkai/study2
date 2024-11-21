# file detection
import os
path = "C:\\Users\\micha\\Downloads"

if os.path.exists(path):
    print("That location exists!")
    if os.path.isfile(path):
        print("That is a file")
    elif os.path.isdir(path):
        print("That is a directory!")
else:
    print("That location dosn't exist!")

# output: 
# That location exists!
# That is a directory!