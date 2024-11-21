# without inhheritence, so no need for animal class
class Rabbit:
    alive = True

    def eat(self):
        print("This rabbit is eating")

    def slumber(self):
        print("This rabbit is sleeping")

class Fish:
    alive = True

    def eat(self):
        print("This fish is eating")

    def slumber(self):
        print("This fish is sleeping") 

class Hawk:
    def eat(self):
        print("This hawk is eating")

    def slumber(self):
        print("This hawk is sleeping")

rabbit = Rabbit()
fish = Fish()
hawk = Hawk()

print(rabbit.alive)
fish.eat()
hawk.slumber()
