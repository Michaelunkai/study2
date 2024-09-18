# Dictionaries and More Complex Functions

# Dictionaries
studio_info = {'name': 'John', 'age': 20, 'grade': 'a'}
print('Student Info:', studio_info)

# Complex Functions
def calculate_area(shape, **kwargs):
    if shape == "rectangle":
        return kwargs['length'] * kwargs['width']
    elif shape == 'circle':
        return 3.14 * (kwargs['radius'] ** 2)
   
# Calculate area
rectangle_area = calculate_area("rectangle", length=5, width=3)
circle_area = calculate_area("circle", radius=4)

print("Rectangle Area:", rectangle_area)
print("Circle Area:", circle_area)

# output:
# Student Info: {'name': 'John', 'age': 20, 'grade': 'a'}
# Rectangle Area: 15
# Circle Area: 50.24