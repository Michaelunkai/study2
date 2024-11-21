# method chaining
# Calling multiple methods in a single line, each 
# affecting the object, enabling concise code.

class Car:

    def turn_on(self):
        print("You start the engine")
        return self

    def drive(self):
        print("You drive the car")
        return self

    def brake(self):
        print("You step on the brakes")
        return self

    def turn_off(self):
        print("You turn off the engine")
        return self

car = Car()

car.turn_on()\
    .drive()\
    .brake()\
    .turn_off()