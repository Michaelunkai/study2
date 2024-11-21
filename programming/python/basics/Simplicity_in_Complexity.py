# Simplicity in Complexity


# Step 1: Understanding Recursion
# Title: "Mastering Recursion: Simplicity in Complexity"

# Step 2: Iterative Walking
def iterative_walk(steps):
    for step in range(1, steps + 1):
        print(f"You take step number {step}")

# Invoke the function
iterative_walk(100)

# Step 3: Recursive Walking
def recursive_walk(steps):
    if steps == 0:
        return
    print(f"You take step number {steps}")
    recursive_walk(steps - 1)

# Invoke the function
recursive_walk(100)

# Step 4: Handling Recursion Depth Error
def recursive_walk(steps):
    if steps == 0:
        return
    print(f"You take step number {steps}")
    recursive_walk(steps - 1)

# Invoke the function
recursive_walk(1000)  # Now with proper base condition

# Step 5: Recursion in Factorial
def factorial_iterative(x):
    result = 1
    for y in range(1, x + 1):
        result *= y
    return result

# Invoke the function
print(factorial_iterative(10))

# Step 6: Recursive Factorial
def factorial_recursive(x):
    if x == 1:
        return 1
    else:
        return x * factorial_recursive(x - 1)

# Invoke the function
print(factorial_recursive(10))

# Step 7: Conclusion
# In conclusion, recursion simplifies problem-solving by calling a function within itself.
# It's applicable iteratively or recursively, with considerations for speed.
# Recursion shines in certain scenarios like data structures and algorithms.

# Final Code
def iterative_walk(steps):
    for step in range(1, steps + 1):
        print(f"You take step number {step}")

def recursive_walk(steps):
    if steps == 0:
        return
    print(f"You take step number {steps}")
    recursive_walk(steps - 1)

def factorial_iterative(x):
    result = 1
    for y in range(1, x + 1):
        result *= y
    return result

def factorial_recursive(x):
    if x == 1:
        return 1
    else:
        return x * factorial_recursive(x - 1)

# Invoke the functions
iterative_walk(100)
recursive_walk(1000)
print(factorial_iterative(10))
print(factorial_recursive(10))
