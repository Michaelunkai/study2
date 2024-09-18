# Detectors
# Decorator function
def greeting_decorator(func):
    def wrapper(name):
        return "Greeting, " + func(name) + "!"
    return wrapper

# Applying the decorator
@greeting_decorator
def greet(name):
    return name

# Calling the decorated function
result = greet("Alice")
print(result)
# output: Greeting, Alice!
