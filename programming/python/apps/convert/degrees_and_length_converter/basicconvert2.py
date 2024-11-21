def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def inches_to_centimeters(inches):
    return inches * 2.54

def centimeters_to_inches(centimeters):
    return centimeters / 2.54

def main():
    print("Choose conversion:")
    print("1. Fahrenheit to Celsius")
    print("2. Celsius to Fahrenheit")
    print("3. Inches to Centimeters")
    print("4. Centimeters to Inches")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        temperature_f = float(input("Enter temperature in Fahrenheit: "))
        temperature_c = fahrenheit_to_celsius(temperature_f)
        print(f"{temperature_f} Fahrenheit is equal to {temperature_c:.2f} Celsius")
    elif choice == 2:
        temperature_c = float(input("Enter temperature in Celsius: "))
        temperature_f = celsius_to_fahrenheit(temperature_c)
        print(f"{temperature_c} Celsius is equal to {temperature_f:.2f} Fahrenheit")
    elif choice == 3:
        length_inches = float(input("Enter length in inches: "))
        length_cm = inches_to_centimeters(length_inches)
        print(f"{length_inches} inches is equal to {length_cm:.2f} centimeters")
    elif choice == 4:
        length_cm = float(input("Enter length in centimeters: "))
        length_inches = centimeters_to_inches(length_cm)
        print(f"{length_cm} centimeters is equal to {length_inches:.2f} inches")
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
