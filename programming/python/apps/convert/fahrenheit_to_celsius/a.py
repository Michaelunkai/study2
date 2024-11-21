def fahrenheit_to_celsius():
    # Prompt the user to enter a number in Fahrenheit
    fahrenheit = float(input("Enter number in Fahrenheit to convert to Celsius: "))
    # Convert Fahrenheit to Celsius using the formula: (F - 32) * 5/9
    celsius = (fahrenheit - 32) * 5/9
    # Display the result
    print(f"{fahrenheit}°F is {celsius:.2f}°C")

# Call the function to run the conversion
fahrenheit_to_celsius()
