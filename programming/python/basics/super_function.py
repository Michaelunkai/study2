# super function
# super() calls parent class methods, facilitating inheritance and avoiding hardcoding class names.

class Rectangle:
    
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Square(Rectangle):

    def __init__(self, side_length):
        super().__init__(side_length, side_length)

    def area(self):
        return self.length * self.width

class Cube(Rectangle):

    def __init__(self, side_length, height):
        super().__init__(side_length, side_length)
        self.height = height

    def volume(self):
        return self.length * self.width * self.height

square = Square(3)
cube = Cube(3, 3)

print(square.area())
print(cube.volume())
# output: 9 27

