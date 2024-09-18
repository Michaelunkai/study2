option = int(input("Choose an option:\n1. lbs to kg\n2. kg to lbs\n"))

if option == 1:
    weight_lbs = float(input('Enter wight in pounds: '))
    weight_kg = weight_lbs * 0.45
    print(f'{weight_lbs} = {weight_kg} kg.')
elif option == 2:
    weight_kg = float(input('Enter weight in kilograms: '))
    weight_lbs = weight_kg / 0.45
    print(f'{weight_kg} kg = {weight_lbs} lbs.')
else:
    print('Invalid option. Please choose 1 or 2.')