# delete a file
# import os
# path ="test.txt"
# os.remove('test.txt')

# or:
# import os
# path ="test.txt"
# try:
#     os.remove(path)
# except FileNotFoundError:
#     print("that file is not around, my dude")
# output: that file is not around, my dude

# or:

# import os
# path ="folder"
# try:
#     os.rmdir(path)
# except FileNotFoundError:
#     print("that folder is not around, my dude")
# except PermissionError:
#     print("no permission hommie")
# except OSError:
#     print("You cant delete that, with this funtion")
# else:
#     print(path+" was deleted")
# # output: You cant delete that, with this funtion
    
# or:
import os
import shutil

path ="folder"
try:
    shutil.rmtree(path)
    # this will delete the folder with all the files inside!!
except FileNotFoundError:
    print("that folder is not around, my dude")
except PermissionError:
    print("no permission hommie")
except OSError:
    print("You cant delete that, with this funtion")
else:
    print(path+" was deleted")
# output: You cant delete that, with this funtion
