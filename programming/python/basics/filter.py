# filter
# Filter: Select elements based on a given function's true/false condition.

# Example list of tuples
people = [("Alice", 25),
          ("Bob", 30),
          ("Charlie", 22),
          ("David", 35)]

# Filter people aged 30 and above
filtered_people = list(filter(lambda person: person[1] >= 30, people))

print(filtered_people)

# output:
# [('Bob', 30), ('David', 35)]