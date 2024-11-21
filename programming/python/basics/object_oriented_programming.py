# object oriented programming

class Car:

    def __init__(self,make,model,year,color):
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def drive(self):
        print("This "+self.model+" is driving")

    def stop(self):
        print("This "+self.model+" is stopped")

from car import Car

car_1 = Car("Chevy","Corvette",2021,"blue")
car_2 = Car("Ford","Mustang",2022,"red")

# print(car_1.make)
# print(car_1.model)
# print(car_1.year)
# print(car_1.color)

car_1.drive()
car_1.stop()

