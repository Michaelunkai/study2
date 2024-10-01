def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def inches_to_centimeters(inches):
    return inches * 2.54

def centimeters_to_inches(centimeters):
    return centimeters / 2.54

# Example usage:
temperature_f = 98.6
temperature_c = fahrenheit_to_celsius(temperature_f)
print(f"{temperature_f} Fahrenheit is equal to {temperature_c:.2f} Celsius")

length_inches = 12
length_cm = inches_to_centimeters(length_inches)
print(f"{length_inches} inches is equal to {length_cm:.2f} centimeters")
