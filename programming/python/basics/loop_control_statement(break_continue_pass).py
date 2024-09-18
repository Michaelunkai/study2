# # # loop control statement = change a loops execution from its normal sequence

# # # break =   used to terminate the loop entirely
# # # continue =    skips to the next iteration of the loop.
# # # pass = does nothing, acts as a placeholder

# # while True:
# #     name = input('enter your name: ')
# #     if name != '':
# #         break
# # #  the loop will break only after typing a name

# # continue:

# phone_number ='123-456-7890'

# for i in phone_number:
#     if i == '-':
#         continue
#     print(i)
# # this will print all the numbers sin the variable without the dashes, what line per number
phone_number ='123-456-7890'

for i in phone_number:
    if i == '-':
        continue
    print(i, end='')
#  this will print: 1234567890

# pass (do nothing):
for i in range(1,21):

    if i == 13:
        pass
    else:
        print(i)
# this will print 1-20, each number in its own line, and skip the number 13

