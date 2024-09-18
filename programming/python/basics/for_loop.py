# # # # # # for loop =    a statement that will exececute it's block of code
# # # # # #               a limited amount of times
# # # # # # 
# # # # # #               while loop = unlimited
# # # # # #               for loop = limited


# # # # # # for loop that will count to 10:
# # # # # for i in range(10):
# # # # #     print(i)
# # # # # # i = short for index
# # # # # this code will run 1-9

# # # # for i in range(10):
# # # #     print(i+1)
# # # # # this code will run 1-10

# # # # count a range bewtween 2 numbers:
# # # for i in range(50,100):
# # #     print(i)

# # # add function to count up or down:
# # for i in range(50,100,2):
# #     print(i)
# # # this will count 50-98 with 2 steps every time. to count till 100 use 100+1 instead of 100

# # this loop will print each letter in my name one by one:
# for i in 'Misha':
#     print(i)

# count from 10 to 0:
import time
for seconds in range(10,0,-1):
    print(seconds)
    time.sleep(1)
print('Happy new year!')
# this code will run countdown from 10 to 10 with 1 sec between each number and than print 'happy new year!'