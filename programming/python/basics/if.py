# Welcome message
print("Hello, welcome to Misha's coffee!!!!!")

# User's name
name = input("What's your name?\n")

# Check for "Ben"
if name == "Ben":
    print("You're not welcome here, Evil Ben!! Get out!!")
    exit()
else:
    print("Hello " + name + ", thank you so much for coming today!!\n\n\n")

# Coffee menu
menu = "Black coffee, Espresso, Latte, Cappuccino"
print(name + ", what would you like from our menu today? Here is what we are serving:\n" + menu)
order = input()

# Coffee quantity
price = 8
quantity = input("How many coffees would you like?\n")
total = price * int(quantity)

# Total price
print("Thank you, your total is: $" + str(total))

# Order confirmation
print("Sound good " + name + "? We'll have your " + quantity + " " + order + "(s) ready for you in a moment.")