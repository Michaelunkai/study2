# # write a file 
# text = "uh no!!!"

# with open('test.txt', 'w') as file:
#     file.write(text)

# #  will create file named "test.txt" in current path with the
# #  text i defined.

# write a file 
text = "have good day!"

# this woll do same it append mode instead of write mode:
with open('test.txt', 'a') as file:
    file.write(text)

#  will create file named "test.txt" in current path with the
#  text i defined.