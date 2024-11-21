#  Object-Oriented Programming (OOP)
# Class and Object
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def make_sound(self):
        print(self.name + ' says ' + self.sound)

# Inheritance
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, 'woof')
        self.breed = breed

    def fetch(self):
        print(self.name + ' is fetching.')

# Create objects
cat = Animal("Whiskers", "Meow")
dog = Dog("Buddy", "Golden Retriever")

#  User methods
cat.make_sound()
dog.make_sound()
dog.fetch()

# output:
# Whiskers says Meow
# Buddy says woof
# Buddy is fetching.