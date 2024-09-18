# Async Programming with async and await

import asyncio

# Asynchronous function
async def greet_async(name):
    print("Hello, " + name)
    await asyncio.sleep(1)
    print("Goodbye, " + name)

# Asynchronous execution
async def main():
    await asyncio.gather(
        greet_async("Alice"),
        greet_async("Bob")
    )

# Run the asynchronous program
asyncio.run(main())

# output: 
# Hello, Alice
# Hello, Bob
# Goodbye, Alice
# Goodbye, Bob

# In this step, we're exploring asynchronous programming with the async and await keywords. Asynchronous functions allow non-blocking execution, and the asyncio module is used to run the asynchronous program. The asyncio.sleep(1) simulates an asynchronous delay.