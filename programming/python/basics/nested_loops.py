# nested loops =    the 'inner loop' will finish all of it's iterations before
#           finishing one iteration of 'outer loop'
# nested loop = loop inside of a loop

# rows = int(input('How many rows?: '))
# columns = int(input('How many columns?'))

#  a rectangle made of certain symbol that i choose with nested loop:

rows = int(input('How many rows?: '))
columns = int(input('How many columns?: '))
symbol = input('Enter a symbol to use: ')

for i in range(rows):
    for j in range(columns):
        print(symbol, end='')
    print()