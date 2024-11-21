
def meters_to_feet(meters):

    feet = meters * 3.28084

    return feet

meters_input = float(input("Enter a distance in meters: "))
print(f"{meters_input} meters is {meters_to_feet(meters_input)} feet.")
