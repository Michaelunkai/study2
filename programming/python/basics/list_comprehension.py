# # list comprehension
# # List comprehension in Python is concise syntax for creating lists, combining
# #  loops and conditions, 
# # making code efficient and readable.

# # squares = [] #create an empty list
# # for i in range(1,11): #create a for loop
# #     squares.append(i * i) # define what each loop iteration should be
# # print(squares)
# # output: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# # same, with list comprehension:

# squares = [i * i for i in range(1,11)]
# print(squares)

# students = [100,90,80,70,60,50,40,30,0]

# passed_students = list(filter(lambda x: x >= 60, students))

# print(passed_students)

# with it:

# students = [100,90,80,70,60,50,40,30,0]

# passed_students = [i for i in students if i >= 60]

# print(passed_students)

# _____________________-- with if/else statement:

students = [100,90,80,70,60,50,40,30,0]

passed_students = [i if i >= 60 else "FAILED" for i in students]

print(passed_students)

# output: [100, 90, 80, 70, 60, 'FAILED', 'FAILED', 'FAILED', 'FAILED']