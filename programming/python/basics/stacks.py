# # Step 1: Introduction to Stack
# # A stack is a collection of elements with two main principal operations: push, which adds an element to the collection, and pop, which removes the most recently added element that was not yet removed.

# # In Python, you can implement a basic stack using a list:

# # stack = []

# # # push operation
# # stack.append(1)
# # stack.append(2)
# # stack.append(3)

# # # Pop operation
# # popped_element = stack.pop
# # print('popped element', popped_element)

# # # Current stack
# # print('Current stack', stack)

# # output: 
# # popped element <built-in method pop of list object at 0x0000020F96AAD1C0>
# # Current stack [1, 2, 3]


# # Step 2: Implementing a Stack Class
# # # Now, let's create a simple Stack class to encapsulate these operations:
# # class Stack:
# #     def __init__(self):
# #         self.items = []

# #     def push(self, item):
# #         self.items.append(item)

# #     def pop(self):
# #         return self.items.pop()

# # # Example usage
# # stack = Stack()
# # stack.push(1)
# # stack.push(2)
# # stack.push(3)

# # popped_element = stack.pop()
# # print("Popped element:", popped_element)

# # print("Current stack:", stack.items)

# # # output: 
# # Popped element: 3
# # Current stack: [1, 2]

# # Step 3: Adding a Peek Method
# # Peek allows you to view the top element
# # without removing it:

# # class Stack:
# #     def __init__(self):
# #         self.items = []

# #     def push(self, item):
# #         self.items.append(item)

# #     def pop(self):
# #         return self.items.pop()

# #     def peek(self):
# #         return self.items[-1] if self.items else None

# # # Example usage
# # stack = Stack()
# # stack.push(1)
# # stack.push(2)
# # stack.push(3)

# # top_element = stack.peek()
# # print("Top element:", top_element)

# # print("Current stack:", stack.items)

# # Step 4: Handling Underflow
# # Let's add a check for stack underflow when popping from an empty stack:

# class Stack:
#     def __init__(self):
#         self.items = []

#     def push(self, item):
#         self.items.append(item)

#     def pop(self):
#         if not self.is_empty():
#             return self.items.pop()
#         else:
#             print("Stack underflow: cannot pop from an empty stack.")
#             return None

#     def peek(self):
#         return self.items[-1] if self.items else None

#     def is_empty(self):
#         return len(self.items) == 0

# # Example usage
# stack = Stack()
# popped_element = stack.pop()  # Try popping from an empty stack
# print("Popped element:", popped_element)

# Step 5: Handling Overflow
# Let's add a maximum size to our stack to prevent overflow:

class Stack:
    def __init__(self, max_size=None):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if self.max_size is None or len(self.items) < self.max_size:
            self.items.append(item)
        else:
            print("Stack overflow: cannot push onto a full stack.")

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            print("Stack underflow: cannot pop from an empty stack.")
            return None

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

# Example usage
stack = Stack(max_size=3)
stack.push(1)
stack.push(2)
stack.push(3)
stack.push(4)  # Try pushing onto a full stack
print("Current stack:", stack.items)
