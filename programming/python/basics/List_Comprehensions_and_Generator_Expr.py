# List Comprehensions and Generator Expressions
squares = [x ** 2 for x in range(1, 6)]
print("Squares: ", squares)  # output: Squares:  [1, 4, 9, 16, 25]

# Generator Expression for even numbers
even_numbers = (x for x in range(10) if x % 2 == 0)
print("Even numbers:", list(even_numbers))
# output: Squares:  [1, 4, 9, 16, 25]
# Even numbers: [0, 2, 4, 6, 8]