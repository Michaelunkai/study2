# Function with default parameters
def greet(name, greeting="Hello"):
    return greeting + ", " + name + "!"

# calling the function
print(greet("Alice")) # Output: Hello, Alice!
print(greet("Bob", "Good morning"))  # Output: Good morning, Bob!

# In this step, we're exploring functions with default parameters. 
# The greet function takes a name parameter and an optional greeting parameter with a default value of "Hello".
# This allows flexibility when calling the function, as you can provide a custom greeting or use the default one.