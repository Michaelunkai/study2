print("Hello, welcome to misha's coffee!!!!!")
name = input("whats your name?\n")
print("Hello " + name + ", thank you so much for coming today!!\n\n\n")
menu = "Black coffee, Espresso, Latte, Cappucino"
print(name + ",what would you like from our menu today? here is what we are serving:\n" + menu)
order = input()
price = 8
quantity = input("How many coffees would you like?\n")
total = price * int(quantity)
print("thank you, your total is: $" + str(total))
print("Sound good " + name + ", we'll have your " + quantity + " " + order + " ready for you in a moment.")
