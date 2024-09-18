class Car:
    # class variables
    wheels = 4  # class variable

    def __init__(self, make, model, year, color):
        self.make = make  # instance variable
        self.model = model  # instance variable
        self.year = year  # instance variable
        self.color = color  # instance variable

# car_1 = Car("Chevy", "Corvette", 2021, "blue")
# car_2 = Car("Ford", "Mustang", 2022, "red")

# car_1.wheels = 2

# print(car_1.wheels)
# print(car_2.wheels)

print(Car.wheels)

car_1 = Car("Chevy", "Corvette", 2021, "blue")
car_2 = Car("Ford", "Mustang", 2022, "red")

Car.wheels = 2

print(car_1.wheels)
print(car_2.wheels)

# instance variable is decleared inside of
# constructor, and they can be giving unique 
# values.


# class variables are decleared within a class
# but outside of the constructor, and i can set 
#  a default value for all instances of this 
# class, for all unique objects that are created 
# and i can change this values later.