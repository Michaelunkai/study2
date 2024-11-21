# logical operators (and,or,not) = used to check if two or more conditional statements are true

# temp = int(input('what is the temp outside?: '))

# if temp >= 0 and temp <=30:
#     print('the temp is nice today!')
#     print('lets go outside!!')
# elif temp < 0 or temp >30:
#     print('the temp sucks today')
#     print('stay inside!!')

# the 'not' logical operator will take a conditional statement and flip it (from true to false, and from normally false to true:

temp = int(input('what is the temp outside?: '))

if not(temp >= 0 and temp <=30):
       print('the temp sucks today')
       print('stay inside!!')

elif not(temp < 0 or temp >30):
    print('the temp is nice today!')
    print('lets go outside!!')