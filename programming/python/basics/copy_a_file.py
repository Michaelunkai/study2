#  copy a file

# copyfile() = copies contents a file
# copy() = copyfile() + permission mode + destination can be a directory
# copy2() = copy() + copies metadata (file's creation and modification times)

import  util

 util.copyfile('test.txt','copy.txt') #sec.dst
# this will copt 'test.txt' file as 'copy.txt'