# sort

# sort() method = used with lists
# sort() function = used with iterables

# students = ["Squidwards","Sandy","Patrick"] 

# # students.sort(reverse=True)
# sorted_students = sorted(students)

# for i in sorted_students:
#     print(i)

# students = [("Squidward", "F", 60),
#             ("Sandy", "A", 33),
#             ("Patrick","D", 36)]

# students.sort()

# for i in students:
#     print(i)

# output: 
#     ('Patrick', 'D', 36)
# ('Sandy', 'A', 33)
# ('Squidward', 'F', 60)

# students = [("Squidward", "F", 60),
#             ("Sandy", "A", 33),
#             ("Patrick","D", 36)]

# grade = lambda grades:grades[1]
# students.sort(key=grade)

# for i in students:
#     print(i)

# in reverase:
students = [("Squidward", "F", 60),
            ("Sandy", "A", 33),
            ("Patrick","D", 36)]

grade = lambda grades:grades[1]
students.sort(key=grade,reverse=True)

for i in students:
    print(i)